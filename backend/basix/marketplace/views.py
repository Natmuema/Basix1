from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Sum, Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import (
    Creator, Product, NFT, Utility, Ownership, DynamicOwnership,
    GovernanceVote, UtilityGate, ImpactScore, FundingThreshold,
    NFTHistory, MarketplaceStats
)
from .serializers import (
    CreatorSerializer, CreatorDetailSerializer, ProductSerializer, ProductDetailSerializer,
    NFTSerializer, NFTDetailSerializer, UtilitySerializer, OwnershipSerializer,
    DynamicOwnershipSerializer, GovernanceVoteSerializer, UtilityGateSerializer,
    ImpactScoreSerializer, FundingThresholdSerializer, NFTHistorySerializer,
    MarketplaceStatsSerializer, NFTMintSerializer, NFTTransferSerializer,
    ImpactScoreCalculationSerializer
)


class CreatorViewSet(viewsets.ModelViewSet):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['reputation_score']
    search_fields = ['user__username', 'user__email', 'wallet_address', 'bio']
    ordering_fields = ['reputation_score', 'created_at', 'updated_at']
    ordering = ['-reputation_score']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CreatorDetailSerializer
        return CreatorSerializer

    @action(detail=True, methods=['get'])
    def nfts(self, request, pk=None):
        """Get all NFTs created by a specific creator"""
        creator = self.get_object()
        nfts = NFT.objects.filter(creator=creator)
        serializer = NFTSerializer(nfts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Get all products created by a specific creator"""
        creator = self.get_object()
        products = Product.objects.filter(creator=creator)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def ownerships(self, request, pk=None):
        """Get all ownership stakes of a specific creator"""
        creator = self.get_object()
        ownerships = Ownership.objects.filter(creator=creator)
        serializer = OwnershipSerializer(ownerships, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_reputation(self, request, pk=None):
        """Update creator reputation score"""
        creator = self.get_object()
        new_score = request.data.get('reputation_score')
        if new_score is not None and 0 <= new_score <= 100:
            creator.reputation_score = new_score
            creator.save()
            serializer = self.get_serializer(creator)
            return Response(serializer.data)
        return Response(
            {'error': 'Invalid reputation score'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product_type', 'category', 'is_physical', 'is_digital', 'creator']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer

    @action(detail=True, methods=['get'])
    def nft(self, request, pk=None):
        """Get the NFT associated with this product"""
        product = self.get_object()
        try:
            nft = product.nft
            serializer = NFTSerializer(nft)
            return Response(serializer.data)
        except NFT.DoesNotExist:
            return Response(
                {'error': 'No NFT found for this product'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class NFTViewSet(viewsets.ModelViewSet):
    queryset = NFT.objects.all()
    serializer_class = NFTSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_minted', 'is_listed', 'blockchain', 'creator']
    search_fields = ['token_id', 'product__name']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NFTDetailSerializer
        return NFTSerializer

    @action(detail=True, methods=['post'])
    def mint(self, request, pk=None):
        """Mint an NFT"""
        nft = self.get_object()
        serializer = NFTMintSerializer(data=request.data)
        if serializer.is_valid():
            nft.is_minted = True
            nft.token_id = serializer.validated_data.get('token_id', nft.token_id)
            nft.metadata_uri = serializer.validated_data.get('metadata_uri', nft.metadata_uri)
            nft.blockchain = serializer.validated_data.get('blockchain', nft.blockchain)
            nft.contract_address = serializer.validated_data.get('contract_address', nft.contract_address)
            nft.save()
            
            # Add to history
            NFTHistory.objects.create(
                nft=nft,
                action_type='mint',
                action_description=f'NFT minted on {nft.blockchain}',
                user=request.user
            )
            
            serializer = self.get_serializer(nft)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def list_for_sale(self, request, pk=None):
        """List NFT for sale"""
        nft = self.get_object()
        nft.is_listed = True
        nft.save()
        
        NFTHistory.objects.create(
            nft=nft,
            action_type='sale',
            action_description='NFT listed for sale',
            user=request.user
        )
        
        serializer = self.get_serializer(nft)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def transfer_ownership(self, request, pk=None):
        """Transfer ownership of an NFT"""
        nft = self.get_object()
        serializer = NFTTransferSerializer(data=request.data)
        if serializer.is_valid():
            from_creator_id = serializer.validated_data['from_creator_id']
            to_creator_id = serializer.validated_data['to_creator_id']
            percentage = serializer.validated_data['percentage']
            
            # Update ownership
            from_ownership = Ownership.objects.get(nft=nft, creator_id=from_creator_id)
            to_creator = Creator.objects.get(id=to_creator_id)
            
            if from_ownership.percentage >= percentage:
                from_ownership.percentage -= percentage
                from_ownership.save()
                
                to_ownership, created = Ownership.objects.get_or_create(
                    nft=nft, creator=to_creator,
                    defaults={'percentage': percentage}
                )
                if not created:
                    to_ownership.percentage += percentage
                    to_ownership.save()
                
                NFTHistory.objects.create(
                    nft=nft,
                    action_type='transfer',
                    action_description=f'Transferred {percentage}% ownership',
                    user=request.user,
                    metadata={'from': from_creator_id, 'to': to_creator_id}
                )
                
                serializer = self.get_serializer(nft)
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'Insufficient ownership percentage'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def utilities(self, request, pk=None):
        """Get all utilities for an NFT"""
        nft = self.get_object()
        utilities = nft.utilities.all()
        serializer = UtilitySerializer(utilities, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def ownerships(self, request, pk=None):
        """Get all ownership stakes for an NFT"""
        nft = self.get_object()
        ownerships = nft.ownerships.all()
        serializer = OwnershipSerializer(ownerships, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """Get transaction history for an NFT"""
        nft = self.get_object()
        history = nft.history.all()
        serializer = NFTHistorySerializer(history, many=True)
        return Response(serializer.data)


class UtilityViewSet(viewsets.ModelViewSet):
    queryset = Utility.objects.all()
    serializer_class = UtilitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['utility_type', 'is_active', 'nft']
    search_fields = ['description']


class OwnershipViewSet(viewsets.ModelViewSet):
    queryset = Ownership.objects.all()
    serializer_class = OwnershipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['nft', 'creator', 'is_active']
    ordering_fields = ['percentage', 'created_at']
    ordering = ['-percentage']


class DynamicOwnershipViewSet(viewsets.ModelViewSet):
    queryset = DynamicOwnership.objects.all()
    serializer_class = DynamicOwnershipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['nft', 'rule_type', 'is_active']
    search_fields = ['rule_description']


class GovernanceVoteViewSet(viewsets.ModelViewSet):
    queryset = GovernanceVote.objects.all()
    serializer_class = GovernanceVoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['nft', 'creator', 'is_reputation_weighted']
    ordering_fields = ['weight', 'vote_timestamp']
    ordering = ['-vote_timestamp']


class UtilityGateViewSet(viewsets.ModelViewSet):
    queryset = UtilityGate.objects.all()
    serializer_class = UtilityGateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['nft', 'utility', 'is_active']
    search_fields = ['condition']


class ImpactScoreViewSet(viewsets.ModelViewSet):
    queryset = ImpactScore.objects.all()
    serializer_class = ImpactScoreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['nft']
    ordering_fields = ['heritage_value', 'sustainability_score', 'calculated_at']
    ordering = ['-heritage_value']

    @action(detail=True, methods=['post'])
    def recalculate(self, request, pk=None):
        """Recalculate impact score"""
        impact_score = self.get_object()
        serializer = ImpactScoreCalculationSerializer(data=request.data)
        if serializer.is_valid():
            impact_score.heritage_value = serializer.validated_data['heritage_value']
            impact_score.sustainability_score = serializer.validated_data['sustainability_score']
            impact_score.sdg_alignment = serializer.validated_data.get('sdg_alignment', [])
            impact_score.save()
            
            serializer = self.get_serializer(impact_score)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FundingThresholdViewSet(viewsets.ModelViewSet):
    queryset = FundingThreshold.objects.all()
    serializer_class = FundingThresholdSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['nft', 'currency', 'is_active']
    ordering_fields = ['amount', 'created_at']
    ordering = ['-amount']


class NFTHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NFTHistory.objects.all()
    serializer_class = NFTHistorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['nft', 'action_type', 'user']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']


class MarketplaceStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MarketplaceStats.objects.all()
    serializer_class = MarketplaceStatsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current marketplace statistics"""
        stats, created = MarketplaceStats.objects.get_or_create(
            id=1,
            defaults={
                'total_nfts': NFT.objects.count(),
                'total_creators': Creator.objects.count(),
                'total_volume': 0,
                'active_listings': NFT.objects.filter(is_listed=True).count()
            }
        )
        
        if not created:
            # Update stats
            stats.total_nfts = NFT.objects.count()
            stats.total_creators = Creator.objects.count()
            stats.active_listings = NFT.objects.filter(is_listed=True).count()
            stats.save()
        
        serializer = self.get_serializer(stats)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get detailed marketplace analytics"""
        analytics = {
            'total_nfts': NFT.objects.count(),
            'total_creators': Creator.objects.count(),
            'active_listings': NFT.objects.filter(is_listed=True).count(),
            'minted_nfts': NFT.objects.filter(is_minted=True).count(),
            'products_by_type': Product.objects.values('product_type').annotate(count=Count('id')),
            'nfts_by_blockchain': NFT.objects.values('blockchain').annotate(count=Count('id')),
            'avg_reputation': Creator.objects.aggregate(avg_reputation=Avg('reputation_score')),
            'total_ownership_stakes': Ownership.objects.count(),
            'recent_activity': NFTHistory.objects.order_by('-timestamp')[:10]
        }
        return Response(analytics)