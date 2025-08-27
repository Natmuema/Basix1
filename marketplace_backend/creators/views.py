from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Creator
from .serializers import (
    CreatorSerializer, CreatorCreateSerializer, CreatorSummarySerializer
)
from nfts.models import NFT, Ownership
from utilities.utils import update_creator_reputation


class CreatorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing creators.
    """
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreatorCreateSerializer
        elif self.action == 'list':
            return CreatorSummarySerializer
        return CreatorSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def nfts(self, request, pk=None):
        """Get all NFTs owned by this creator"""
        creator = self.get_object()
        ownerships = Ownership.objects.filter(creator=creator).select_related('nft')
        
        data = []
        for ownership in ownerships:
            data.append({
                'nft_id': ownership.nft.id,
                'nft_name': ownership.nft.name,
                'token_id': ownership.nft.token_id,
                'ownership_percentage': float(ownership.percentage),
                'is_funded': ownership.nft.is_funded,
                'funding_percentage': ownership.nft.funding_percentage
            })
        
        return Response(data)
    
    @action(detail=True, methods=['get'])
    def created_nfts(self, request, pk=None):
        """Get NFTs where this creator is the primary owner (created by them)"""
        creator = self.get_object()
        # Get NFTs where creator has highest ownership percentage
        primary_ownerships = Ownership.objects.filter(
            creator=creator,
            percentage__gte=50  # Assuming primary owner has at least 50%
        ).select_related('nft')
        
        data = []
        for ownership in primary_ownerships:
            data.append({
                'nft_id': ownership.nft.id,
                'nft_name': ownership.nft.name,
                'token_id': ownership.nft.token_id,
                'ownership_percentage': float(ownership.percentage),
                'total_funding': float(ownership.nft.current_funding),
                'funding_threshold': float(ownership.nft.funding_threshold)
            })
        
        return Response(data)
    
    @action(detail=True, methods=['post'])
    def update_reputation(self, request, pk=None):
        """Update creator reputation based on action"""
        creator = self.get_object()
        action_type = request.data.get('action_type')
        value = request.data.get('value', 1)
        
        if not action_type:
            return Response(
                {'error': 'action_type is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        new_reputation = update_creator_reputation(creator, action_type, value)
        
        return Response({
            'new_reputation': new_reputation,
            'message': f'Reputation updated to {new_reputation}'
        })
    
    @action(detail=False, methods=['get'])
    def top_creators(self, request):
        """Get top creators by reputation"""
        limit = int(request.query_params.get('limit', 10))
        creators = Creator.objects.order_by('-reputation_score')[:limit]
        serializer = CreatorSummarySerializer(creators, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def verified(self, request):
        """Get only verified creators (those who have minted NFTs)"""
        creators = Creator.objects.filter(
            nft_ownerships__isnull=False
        ).distinct()
        serializer = self.get_serializer(creators, many=True)
        return Response(serializer.data)