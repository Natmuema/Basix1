from rest_framework import serializers
from .models import Transaction, ImpactMetrics, MarketplaceStats
from nfts.serializers import NFTSerializer
from creators.serializers import CreatorSummarySerializer


class TransactionSerializer(serializers.ModelSerializer):
    nft = serializers.StringRelatedField()
    from_creator = CreatorSummarySerializer(read_only=True)
    to_creator = CreatorSummarySerializer(read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_type', 'nft', 'from_creator', 'to_creator',
            'amount', 'ownership_percentage', 'transaction_hash',
            'block_number', 'metadata', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']


class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'transaction_type', 'nft', 'from_creator', 'to_creator',
            'amount', 'ownership_percentage', 'transaction_hash',
            'block_number', 'metadata'
        ]


class ImpactMetricsSerializer(serializers.ModelSerializer):
    nft_name = serializers.CharField(source='nft.name', read_only=True)
    
    class Meta:
        model = ImpactMetrics
        fields = [
            'id', 'nft', 'nft_name', 'heritage_value', 'sustainability_score',
            'overall_impact_score', 'total_supporters', 'total_funding',
            'transactions_count', 'utilities_redeemed', 'recorded_at'
        ]
        read_only_fields = ['id', 'recorded_at']


class MarketplaceStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceStats
        fields = [
            'id', 'date', 'total_creators', 'verified_creators',
            'average_reputation', 'total_nfts', 'funded_nfts',
            'total_funding_raised', 'total_products', 'products_by_type',
            'daily_transactions', 'daily_volume', 'average_heritage_value',
            'average_sustainability_score', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UtilityAccessSerializer(serializers.Serializer):
    """Check utility access for a creator"""
    creator_id = serializers.IntegerField()
    nft_id = serializers.IntegerField()


class ImpactScoreSerializer(serializers.Serializer):
    """Calculate impact score for an NFT"""
    nft_id = serializers.IntegerField()
    impact_score = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    heritage_value = serializers.IntegerField(read_only=True)
    sustainability_score = serializers.IntegerField(read_only=True)
    creator_reputation_avg = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)