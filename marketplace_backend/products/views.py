from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count, Q
from .models import Product
from .serializers import (
    ProductSerializer, ProductCreateSerializer, ProductSummarySerializer
)


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ProductCreateSerializer
        elif self.action == 'list':
            return ProductSummarySerializer
        return ProductSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Filter by product type
        product_type = self.request.query_params.get('type', None)
        if product_type:
            queryset = queryset.filter(product_type=product_type)
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by properties
        is_physical = self.request.query_params.get('is_physical', None)
        if is_physical is not None:
            queryset = queryset.filter(is_physical=is_physical.lower() == 'true')
        
        is_digital = self.request.query_params.get('is_digital', None)
        if is_digital is not None:
            queryset = queryset.filter(is_digital=is_digital.lower() == 'true')
        
        is_redeemable = self.request.query_params.get('is_redeemable', None)
        if is_redeemable is not None:
            queryset = queryset.filter(is_redeemable=is_redeemable.lower() == 'true')
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def nfts(self, request, pk=None):
        """Get all NFTs linked to this product"""
        product = self.get_object()
        nfts = product.nfts.all()
        
        data = []
        for nft in nfts:
            data.append({
                'id': nft.id,
                'token_id': nft.token_id,
                'name': nft.name,
                'is_funded': nft.is_funded,
                'funding_percentage': nft.funding_percentage,
                'current_funding': float(nft.current_funding),
                'funding_threshold': float(nft.funding_threshold)
            })
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get product statistics by type and category"""
        stats = {
            'by_type': {},
            'by_category': {},
            'total_products': Product.objects.count(),
            'physical_products': Product.objects.filter(is_physical=True).count(),
            'digital_products': Product.objects.filter(is_digital=True).count(),
            'redeemable_products': Product.objects.filter(is_redeemable=True).count()
        }
        
        # Count by product type
        type_counts = Product.objects.values('product_type').annotate(
            count=Count('id')
        )
        for item in type_counts:
            stats['by_type'][item['product_type']] = item['count']
        
        # Count by category
        category_counts = Product.objects.values('category').annotate(
            count=Count('id')
        )
        for item in category_counts:
            stats['by_category'][item['category']] = item['count']
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def cultural_heritage(self, request):
        """Get products related to cultural heritage"""
        cultural_types = ['ArtCraft', 'Music', 'Fashion', 'Heritage']
        products = Product.objects.filter(product_type__in=cultural_types)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def software_products(self, request):
        """Get software products"""
        products = Product.objects.filter(product_type='Software')
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)