from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from .models import NFT, Ownership, Utility, GovernanceVote
from .serializers import (
    NFTSerializer, NFTCreateSerializer, NFTUpdateSerializer,
    NFTHistorySerializer, OwnershipSerializer, UtilitySerializer,
    GovernanceVoteSerializer
)
from creators.models import Creator
from utilities.utils import (
    calculate_ownership_distribution, get_accessible_utilities,
    record_impact_metrics, check_funding_threshold
)


class NFTViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing NFTs.
    """
    queryset = NFT.objects.all()
    serializer_class = NFTSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return NFTCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return NFTUpdateSerializer
        return NFTSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = NFT.objects.all()
        
        # Filter by funded status
        is_funded = self.request.query_params.get('is_funded', None)
        if is_funded is not None:
            if is_funded.lower() == 'true':
                queryset = queryset.filter(current_funding__gte=F('funding_threshold'))
            else:
                queryset = queryset.filter(current_funding__lt=F('funding_threshold'))
        
        # Filter by product type
        product_type = self.request.query_params.get('product_type', None)
        if product_type:
            queryset = queryset.filter(product__product_type=product_type)
        
        # Filter by minimum impact score
        min_impact = self.request.query_params.get('min_impact', None)
        if min_impact:
            # This is a simplified filter - in production you'd calculate on the fly
            min_val = float(min_impact)
            queryset = queryset.filter(
                heritage_value__gte=min_val - 10,
                sustainability_score__gte=min_val - 10
            )
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def append_history(self, request, pk=None):
        """Append an action to NFT history"""
        nft = self.get_object()
        serializer = NFTHistorySerializer(data=request.data)
        
        if serializer.is_valid():
            nft.append_history(
                serializer.validated_data['action'],
                serializer.validated_data.get('details')
            )
            return Response({'message': 'History updated successfully'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def ownership_distribution(self, request, pk=None):
        """Get ownership distribution for an NFT"""
        nft = self.get_object()
        distribution = calculate_ownership_distribution(nft)
        return Response(distribution)
    
    @action(detail=True, methods=['post'])
    def add_ownership(self, request, pk=None):
        """Add or update ownership for an NFT"""
        nft = self.get_object()
        serializer = OwnershipSerializer(data=request.data)
        
        if serializer.is_valid():
            creator = serializer.validated_data['creator']
            
            # Check if ownership already exists
            ownership, created = Ownership.objects.update_or_create(
                nft=nft,
                creator=creator,
                defaults=serializer.validated_data
            )
            
            if created:
                nft.append_history('ownership_added', {
                    'creator_id': creator.id,
                    'percentage': float(serializer.validated_data['percentage'])
                })
            else:
                nft.append_history('ownership_updated', {
                    'creator_id': creator.id,
                    'percentage': float(serializer.validated_data['percentage'])
                })
            
            return Response(
                OwnershipSerializer(ownership).data,
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def add_utility(self, request, pk=None):
        """Add a utility to an NFT"""
        nft = self.get_object()
        serializer = UtilitySerializer(data=request.data)
        
        if serializer.is_valid():
            utility = serializer.save(nft=nft)
            nft.append_history('utility_added', {
                'utility_type': utility.utility_type
            })
            return Response(
                UtilitySerializer(utility).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def accessible_utilities(self, request, pk=None):
        """Get utilities accessible to a specific creator"""
        nft = self.get_object()
        creator_id = request.query_params.get('creator_id')
        
        if not creator_id:
            return Response(
                {'error': 'creator_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        creator = get_object_or_404(Creator, pk=creator_id)
        utilities = get_accessible_utilities(nft, creator)
        serializer = UtilitySerializer(utilities, many=True)
        
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_governance_vote(self, request, pk=None):
        """Add governance voting rights"""
        nft = self.get_object()
        serializer = GovernanceVoteSerializer(data=request.data)
        
        if serializer.is_valid():
            vote, created = GovernanceVote.objects.update_or_create(
                nft=nft,
                creator=serializer.validated_data['creator'],
                defaults=serializer.validated_data
            )
            
            return Response(
                GovernanceVoteSerializer(vote).data,
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def contribute_funding(self, request, pk=None):
        """Contribute funding to an NFT"""
        nft = self.get_object()
        amount = request.data.get('amount')
        
        if not amount:
            return Response(
                {'error': 'amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            return Response(
                {'error': 'amount must be a positive number'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        nft.current_funding += amount
        nft.save()
        
        # Record history
        nft.append_history('funding_contribution', {
            'amount': amount,
            'new_total': float(nft.current_funding)
        })
        
        # Check if funding threshold reached
        if check_funding_threshold(nft):
            nft.append_history('funding_threshold_reached', {
                'threshold': float(nft.funding_threshold)
            })
        
        return Response({
            'current_funding': float(nft.current_funding),
            'funding_threshold': float(nft.funding_threshold),
            'is_funded': nft.is_funded,
            'funding_percentage': nft.funding_percentage
        })
    
    @action(detail=True, methods=['post'])
    def record_metrics(self, request, pk=None):
        """Record current impact metrics for the NFT"""
        nft = self.get_object()
        metrics = record_impact_metrics(nft)
        
        return Response({
            'message': 'Metrics recorded successfully',
            'metrics': {
                'heritage_value': metrics.heritage_value,
                'sustainability_score': metrics.sustainability_score,
                'overall_impact_score': float(metrics.overall_impact_score),
                'total_supporters': metrics.total_supporters,
                'total_funding': float(metrics.total_funding)
            }
        })
    
    @action(detail=False, methods=['get'])
    def top_funded(self, request):
        """Get top funded NFTs"""
        limit = int(request.query_params.get('limit', 10))
        nfts = NFT.objects.filter(
            current_funding__gt=0
        ).order_by('-current_funding')[:limit]
        
        serializer = self.get_serializer(nfts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def high_impact(self, request):
        """Get NFTs with high impact scores"""
        min_score = int(request.query_params.get('min_score', 80))
        nfts = NFT.objects.filter(
            heritage_value__gte=min_score,
            sustainability_score__gte=min_score
        )
        
        serializer = self.get_serializer(nfts, many=True)
        return Response(serializer.data)