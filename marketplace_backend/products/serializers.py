from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    nft_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'product_type', 'description', 'category',
            'is_physical', 'is_digital', 'has_digital_scan', 'is_redeemable',
            'is_license_based', 'image', 'digital_file', 'nft_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_nft_count(self, obj):
        return obj.nfts.count()


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name', 'product_type', 'description', 'category',
            'is_physical', 'is_digital', 'has_digital_scan', 'is_redeemable',
            'is_license_based', 'image', 'digital_file'
        ]


class ProductSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing many products"""
    class Meta:
        model = Product
        fields = ['id', 'name', 'product_type', 'category', 'is_physical', 'is_digital']