from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Creator, Product, NFT, Utility, Ownership, DynamicOwnership,
    GovernanceVote, UtilityGate, ImpactScore, FundingThreshold,
    NFTHistory, MarketplaceStats
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']


class CreatorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Creator
        fields = [
            'id', 'user', 'user_id', 'wallet_address', 'skills', 
            'reputation_score', 'bio', 'profile_image', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_wallet_address(self, value):
        if Creator.objects.filter(wallet_address=value).exists():
            raise serializers.ValidationError("Wallet address already exists.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer(read_only=True)
    creator_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'product_type', 'category', 'description',
            'is_physical', 'is_digital', 'is_redeemable', 'has_digital_scan',
            'is_license_based', 'creator', 'creator_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UtilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Utility
        fields = ['id', 'nft', 'utility_type', 'description', 'is_active']


class OwnershipSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer(read_only=True)
    creator_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Ownership
        fields = [
            'id', 'nft', 'creator', 'creator_id', 'percentage', 
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DynamicOwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicOwnership
        fields = ['id', 'nft', 'rule_type', 'rule_description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class GovernanceVoteSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer(read_only=True)
    creator_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = GovernanceVote
        fields = [
            'id', 'nft', 'creator', 'creator_id', 'weight', 
            'is_reputation_weighted', 'vote_timestamp'
        ]
        read_only_fields = ['id', 'vote_timestamp']


class UtilityGateSerializer(serializers.ModelSerializer):
    utility = UtilitySerializer(read_only=True)
    utility_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = UtilityGate
        fields = ['id', 'nft', 'utility', 'utility_id', 'condition', 'is_active']


class ImpactScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactScore
        fields = [
            'id', 'nft', 'heritage_value', 'sustainability_score', 
            'sdg_alignment', 'calculated_at'
        ]
        read_only_fields = ['id', 'calculated_at']


class FundingThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundingThreshold
        fields = ['id', 'nft', 'amount', 'currency', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class NFTHistorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = NFTHistory
        fields = [
            'id', 'nft', 'action_type', 'action_description', 
            'user', 'timestamp', 'metadata'
        ]
        read_only_fields = ['id', 'timestamp']


class NFTDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    utilities = UtilitySerializer(many=True, read_only=True)
    ownerships = OwnershipSerializer(many=True, read_only=True)
    dynamic_ownership_rules = DynamicOwnershipSerializer(many=True, read_only=True)
    governance_votes = GovernanceVoteSerializer(many=True, read_only=True)
    utility_gates = UtilityGateSerializer(many=True, read_only=True)
    impact_score = ImpactScoreSerializer(read_only=True)
    funding_threshold = FundingThresholdSerializer(read_only=True)
    history = NFTHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = NFT
        fields = [
            'id', 'token_id', 'product', 'creator', 'metadata_uri',
            'blockchain', 'contract_address', 'is_minted', 'is_listed',
            'created_at', 'updated_at', 'utilities', 'ownerships',
            'dynamic_ownership_rules', 'governance_votes', 'utility_gates',
            'impact_score', 'funding_threshold', 'history'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NFTSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    creator = CreatorSerializer(read_only=True)
    utilities = UtilitySerializer(many=True, read_only=True)
    ownerships = OwnershipSerializer(many=True, read_only=True)
    
    class Meta:
        model = NFT
        fields = [
            'id', 'token_id', 'product', 'creator', 'metadata_uri',
            'blockchain', 'contract_address', 'is_minted', 'is_listed',
            'created_at', 'updated_at', 'utilities', 'ownerships'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MarketplaceStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceStats
        fields = [
            'id', 'total_nfts', 'total_creators', 'total_volume',
            'active_listings', 'last_updated'
        ]
        read_only_fields = ['id', 'last_updated']


# Specialized serializers for specific use cases
class CreatorDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    nfts = NFTSerializer(many=True, read_only=True)
    ownerships = OwnershipSerializer(many=True, read_only=True)
    
    class Meta:
        model = Creator
        fields = [
            'id', 'user', 'wallet_address', 'skills', 'reputation_score',
            'bio', 'profile_image', 'created_at', 'updated_at',
            'products', 'nfts', 'ownerships'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductDetailSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer(read_only=True)
    nft = NFTSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'product_type', 'category', 'description',
            'is_physical', 'is_digital', 'is_redeemable', 'has_digital_scan',
            'is_license_based', 'creator', 'nft', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# Bulk operation serializers
class BulkNFTCreateSerializer(serializers.Serializer):
    nfts = NFTSerializer(many=True)


class NFTMintSerializer(serializers.Serializer):
    token_id = serializers.CharField(max_length=255)
    metadata_uri = serializers.URLField(required=False)
    blockchain = serializers.CharField(max_length=50, default='Ethereum')
    contract_address = serializers.CharField(max_length=255, required=False)


class NFTTransferSerializer(serializers.Serializer):
    from_creator_id = serializers.IntegerField()
    to_creator_id = serializers.IntegerField()
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    reason = serializers.CharField(max_length=255, required=False)


class ImpactScoreCalculationSerializer(serializers.Serializer):
    heritage_value = serializers.IntegerField(min_value=0, max_value=100)
    sustainability_score = serializers.IntegerField(min_value=0, max_value=100)
    sdg_alignment = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False
    )