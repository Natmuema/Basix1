from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum, Count, Avg

from .models import (
    Creator, Product, NFT, Utility, Ownership, DynamicOwnership,
    GovernanceVote, UtilityGate, ImpactScore, FundingThreshold,
    NFTHistory, SmartFunction, CreatorStats, MarketplaceConfig
)
from .serializers import (
    CreatorSerializer, DetailedCreatorSerializer, CreatorStatsSerializer,
    ProductSerializer, NFTSerializer, DetailedNFTSerializer, UtilitySerializer,
    OwnershipSerializer, DynamicOwnershipSerializer, GovernanceVoteSerializer,
    UtilityGateSerializer, ImpactScoreSerializer, FundingThresholdSerializer,
    NFTHistorySerializer, SmartFunctionSerializer, MarketplaceConfigSerializer,
    NFTCreationSerializer, OwnershipTransferSerializer, ImpactScoreCalculationSerializer
)


class CreatorViewSet(viewsets.ModelViewSet):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedCreatorSerializer
        return CreatorSerializer

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get detailed statistics for a creator"""
        creator = self.get_object()
        stats, created = CreatorStats.objects.get_or_create(creator=creator)
        
        # Calculate additional stats
        total_products = creator.products.count()
        total_nfts_owned = creator.owned_nfts.count()
        total_votes_cast = creator.votes_cast.count()
        
        return Response({
            'creator': DetailedCreatorSerializer(creator).data,
            'stats': CreatorStatsSerializer(stats).data,
            'calculated_stats': {
                'total_products': total_products,
                'total_nfts_owned': total_nfts_owned,
                'total_votes_cast': total_votes_cast,
            }
        })

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Get all products by a creator"""
        creator = self.get_object()
        products = creator.products.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def owned_nfts(self, request, pk=None):
        """Get all NFTs owned by a creator"""
        creator = self.get_object()
        ownerships = creator.owned_nfts.all()
        serializer = OwnershipSerializer(ownerships, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_creators(self, request):
        """Get top creators by reputation score"""
        creators = Creator.objects.order_by('-reputation_score')[:10]
        serializer = CreatorSerializer(creators, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Filter by product type
        product_type = self.request.query_params.get('product_type', None)
        if product_type:
            queryset = queryset.filter(product_type=product_type)
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by creator
        creator_id = self.request.query_params.get('creator_id', None)
        if creator_id:
            queryset = queryset.filter(creator_id=creator_id)
        
        # Search by name or description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset

    @action(detail=True, methods=['get'])
    def nft(self, request, pk=None):
        """Get NFT associated with a product"""
        product = self.get_object()
        if hasattr(product, 'nft'):
            serializer = NFTSerializer(product.nft)
            return Response(serializer.data)
        return Response({'detail': 'No NFT found for this product'}, status=404)


class NFTViewSet(viewsets.ModelViewSet):
    queryset = NFT.objects.all()
    serializer_class = NFTSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedNFTSerializer
        elif self.action == 'create':
            return NFTCreationSerializer
        return NFTSerializer

    def get_queryset(self):
        queryset = NFT.objects.all()
        
        # Filter by product type
        product_type = self.request.query_params.get('product_type', None)
        if product_type:
            queryset = queryset.filter(product__product_type=product_type)
        
        # Filter by utility type
        utility_type = self.request.query_params.get('utility_type', None)
        if utility_type:
            queryset = queryset.filter(utilities__utility_type=utility_type)
        
        return queryset

    @action(detail=True, methods=['post'])
    def append_history(self, request, pk=None):
        """Append an action to NFT history"""
        nft = self.get_object()
        action_type = request.data.get('action_type')
        action_data = request.data.get('action_data', {})
        performed_by_id = request.data.get('performed_by_id')
        
        if not action_type:
            return Response(
                {'error': 'action_type is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        performed_by = None
        if performed_by_id:
            performed_by = get_object_or_404(Creator, id=performed_by_id)
        
        history_entry = NFTHistory.objects.create(
            nft=nft,
            action_type=action_type,
            action_data=action_data,
            performed_by=performed_by
        )
        
        serializer = NFTHistorySerializer(history_entry)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def calculate_impact_score(self, request, pk=None):
        """Calculate and update impact score for an NFT"""
        nft = self.get_object()
        serializer = ImpactScoreCalculationSerializer(data=request.data)
        
        if serializer.is_valid():
            heritage_value = serializer.validated_data['heritage_value']
            sustainability_score = serializer.validated_data['sustainability_score']
            sdg_alignment = serializer.validated_data['sdg_alignment']
            
            impact_score, created = ImpactScore.objects.get_or_create(nft=nft)
            impact_score.heritage_value = heritage_value
            impact_score.sustainability_score = sustainability_score
            impact_score.sdg_alignment = sdg_alignment
            impact_score.save()
            
            return Response(ImpactScoreSerializer(impact_score).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def transfer_ownership(self, request, pk=None):
        """Transfer ownership of an NFT"""
        nft = self.get_object()
        serializer = OwnershipTransferSerializer(data=request.data)
        
        if serializer.is_valid():
            from_owner = serializer.validated_data['from_owner_id']
            to_owner = serializer.validated_data['to_owner_id']
            percentage = serializer.validated_data['percentage']
            
            with transaction.atomic():
                # Check if from_owner has enough ownership
                from_ownership = get_object_or_404(
                    Ownership, 
                    nft=nft, 
                    owner=from_owner
                )
                
                if from_ownership.percentage < percentage:
                    return Response(
                        {'error': 'Insufficient ownership percentage'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Update from_owner's ownership
                from_ownership.percentage -= percentage
                if from_ownership.percentage <= 0:
                    from_ownership.delete()
                else:
                    from_ownership.save()
                
                # Update or create to_owner's ownership
                to_ownership, created = Ownership.objects.get_or_create(
                    nft=nft,
                    owner=to_owner,
                    defaults={'percentage': percentage}
                )
                
                if not created:
                    to_ownership.percentage += percentage
                    to_ownership.save()
                
                # Record the transfer in history
                NFTHistory.objects.create(
                    nft=nft,
                    action_type='ownership_changed',
                    action_data={
                        'from_owner': from_owner.id,
                        'to_owner': to_owner.id,
                        'percentage': float(percentage)
                    },
                    performed_by=request.user.creator_profile if hasattr(request.user, 'creator_profile') else None
                )
            
            return Response({'message': 'Ownership transferred successfully'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def is_creator(self, request, pk=None):
        """Check if a user is a creator (has minted at least 1 NFT)"""
        nft = self.get_object()
        creator = nft.product.creator
        total_nfts = creator.products.count()
        
        return Response({
            'creator_id': creator.id,
            'creator_name': creator.user.username,
            'is_creator': total_nfts >= 1,
            'total_nfts_created': total_nfts
        })


class UtilityViewSet(viewsets.ModelViewSet):
    queryset = Utility.objects.all()
    serializer_class = UtilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Utility.objects.all()
        
        # Filter by NFT
        nft_id = self.request.query_params.get('nft_id', None)
        if nft_id:
            queryset = queryset.filter(nft_id=nft_id)
        
        # Filter by utility type
        utility_type = self.request.query_params.get('utility_type', None)
        if utility_type:
            queryset = queryset.filter(utility_type=utility_type)
        
        return queryset


class OwnershipViewSet(viewsets.ModelViewSet):
    queryset = Ownership.objects.all()
    serializer_class = OwnershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Ownership.objects.all()
        
        # Filter by NFT
        nft_id = self.request.query_params.get('nft_id', None)
        if nft_id:
            queryset = queryset.filter(nft_id=nft_id)
        
        # Filter by owner
        owner_id = self.request.query_params.get('owner_id', None)
        if owner_id:
            queryset = queryset.filter(owner_id=owner_id)
        
        return queryset


class DynamicOwnershipViewSet(viewsets.ModelViewSet):
    queryset = DynamicOwnership.objects.all()
    serializer_class = DynamicOwnershipSerializer
    permission_classes = [permissions.IsAuthenticated]


class GovernanceVoteViewSet(viewsets.ModelViewSet):
    queryset = GovernanceVote.objects.all()
    serializer_class = GovernanceVoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = GovernanceVote.objects.all()
        
        # Filter by NFT
        nft_id = self.request.query_params.get('nft_id', None)
        if nft_id:
            queryset = queryset.filter(nft_id=nft_id)
        
        # Filter by voter
        voter_id = self.request.query_params.get('voter_id', None)
        if voter_id:
            queryset = queryset.filter(voter_id=voter_id)
        
        return queryset


class UtilityGateViewSet(viewsets.ModelViewSet):
    queryset = UtilityGate.objects.all()
    serializer_class = UtilityGateSerializer
    permission_classes = [permissions.IsAuthenticated]


class ImpactScoreViewSet(viewsets.ModelViewSet):
    queryset = ImpactScore.objects.all()
    serializer_class = ImpactScoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def top_impact(self, request):
        """Get NFTs with highest impact scores"""
        impact_scores = ImpactScore.objects.order_by(
            '-heritage_value', '-sustainability_score'
        )[:10]
        serializer = ImpactScoreSerializer(impact_scores, many=True)
        return Response(serializer.data)


class FundingThresholdViewSet(viewsets.ModelViewSet):
    queryset = FundingThreshold.objects.all()
    serializer_class = FundingThresholdSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def check_threshold(self, request, pk=None):
        """Check if funding threshold is met"""
        threshold = self.get_object()
        current_amount = request.data.get('current_amount', 0)
        
        if current_amount >= threshold.amount and not threshold.is_met:
            threshold.is_met = True
            threshold.met_at = timezone.now()
            threshold.save()
            
            # Record in NFT history
            NFTHistory.objects.create(
                nft=threshold.nft,
                action_type='funding_met',
                action_data={'amount': float(current_amount)}
            )
        
        return Response({
            'threshold_met': threshold.is_met,
            'required_amount': float(threshold.amount),
            'current_amount': current_amount,
            'remaining': max(0, float(threshold.amount) - current_amount)
        })


class NFTHistoryViewSet(viewsets.ModelViewSet):
    queryset = NFTHistory.objects.all()
    serializer_class = NFTHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = NFTHistory.objects.all()
        
        # Filter by NFT
        nft_id = self.request.query_params.get('nft_id', None)
        if nft_id:
            queryset = queryset.filter(nft_id=nft_id)
        
        # Filter by action type
        action_type = self.request.query_params.get('action_type', None)
        if action_type:
            queryset = queryset.filter(action_type=action_type)
        
        return queryset


class SmartFunctionViewSet(viewsets.ModelViewSet):
    queryset = SmartFunction.objects.all()
    serializer_class = SmartFunctionSerializer
    permission_classes = [permissions.IsAuthenticated]


class MarketplaceConfigViewSet(viewsets.ModelViewSet):
    queryset = MarketplaceConfig.objects.all()
    serializer_class = MarketplaceConfigSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def get_config(self, request):
        """Get configuration by key"""
        key = request.query_params.get('key', None)
        if key:
            config = get_object_or_404(MarketplaceConfig, key=key, is_active=True)
            return Response(config.value)
        
        # Return all active configs
        configs = MarketplaceConfig.objects.filter(is_active=True)
        return Response({
            config.key: config.value for config in configs
        })


# Additional specialized views
class MarketplaceStatsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get marketplace overview statistics"""
        total_creators = Creator.objects.count()
        total_products = Product.objects.count()
        total_nfts = NFT.objects.count()
        total_utilities = Utility.objects.count()
        
        # Calculate total market value (sum of all NFT prices)
        total_market_value = Product.objects.filter(
            price__isnull=False
        ).aggregate(
            total=Sum('price')
        )['total'] or 0
        
        # Get top creators by reputation
        top_creators = Creator.objects.order_by('-reputation_score')[:5]
        
        # Get recent NFTs
        recent_nfts = NFT.objects.order_by('-created_at')[:5]
        
        return Response({
            'total_creators': total_creators,
            'total_products': total_products,
            'total_nfts': total_nfts,
            'total_utilities': total_utilities,
            'total_market_value': float(total_market_value),
            'top_creators': CreatorSerializer(top_creators, many=True).data,
            'recent_nfts': NFTSerializer(recent_nfts, many=True).data,
        })

    @action(detail=False, methods=['get'])
    def product_types_distribution(self, request):
        """Get distribution of products by type"""
        distribution = Product.objects.values('product_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return Response(distribution)

    @action(detail=False, methods=['get'])
    def utility_types_distribution(self, request):
        """Get distribution of utilities by type"""
        distribution = Utility.objects.values('utility_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return Response(distribution)