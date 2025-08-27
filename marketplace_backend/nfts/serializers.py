from rest_framework import serializers
from .models import NFT, Ownership, Utility, GovernanceVote
from creators.models import Creator
from products.models import Product
from utilities.utils import calculate_impact_score


class UtilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Utility
        fields = [
            'id', 'utility_type', 'description', 'ownership_requirement',
            'condition', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class OwnershipSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source='creator.user.username', read_only=True)
    creator_wallet = serializers.CharField(source='creator.wallet_address', read_only=True)
    creator_reputation = serializers.IntegerField(source='creator.reputation_score', read_only=True)
    creator_id = serializers.PrimaryKeyRelatedField(
        queryset=Creator.objects.all(),
        source='creator',
        write_only=True
    )
    
    class Meta:
        model = Ownership
        fields = [
            'id', 'creator_id', 'creator_username', 'creator_wallet', 
            'creator_reputation', 'percentage', 'transfer_rule', 'decay_rule', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class GovernanceVoteSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source='creator.user.username', read_only=True)
    creator_wallet = serializers.CharField(source='creator.wallet_address', read_only=True)
    creator_reputation = serializers.IntegerField(source='creator.reputation_score', read_only=True)
    creator_id = serializers.PrimaryKeyRelatedField(
        queryset=Creator.objects.all(),
        source='creator',
        write_only=True
    )
    effective_weight = serializers.ReadOnlyField()
    
    class Meta:
        model = GovernanceVote
        fields = [
            'id', 'creator_id', 'creator_username', 'creator_wallet',
            'creator_reputation', 'weight', 'is_reputation_weighted', 
            'effective_weight', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class NFTSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_type = serializers.CharField(source='product.product_type', read_only=True)
    product_category = serializers.CharField(source='product.category', read_only=True)
    
    utilities = UtilitySerializer(many=True, read_only=True)
    ownerships = OwnershipSerializer(many=True, read_only=True)
    governance_votes = GovernanceVoteSerializer(many=True, read_only=True)
    
    is_funded = serializers.ReadOnlyField()
    funding_percentage = serializers.ReadOnlyField()
    impact_score = serializers.SerializerMethodField()
    
    class Meta:
        model = NFT
        fields = [
            'id', 'token_id', 'name', 'product', 'product_name', 'product_type',
            'product_category', 'contract_address', 'metadata_uri', 
            'funding_threshold', 'current_funding', 'is_funded', 'funding_percentage', 
            'heritage_value', 'sustainability_score', 'sdg_alignment', 'impact_score',
            'history', 'utilities', 'ownerships', 'governance_votes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_impact_score(self, obj):
        return calculate_impact_score(obj)


class NFTCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product'
    )
    utilities = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = NFT
        fields = [
            'token_id', 'name', 'product_id', 'contract_address',
            'metadata_uri', 'funding_threshold', 'heritage_value',
            'sustainability_score', 'sdg_alignment', 'utilities'
        ]
    
    def create(self, validated_data):
        utilities_data = validated_data.pop('utilities', [])
        nft = NFT.objects.create(**validated_data)
        
        # Create utilities
        for utility_type in utilities_data:
            Utility.objects.create(nft=nft, utility_type=utility_type)
        
        return nft


class NFTUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFT
        fields = [
            'name', 'contract_address', 'metadata_uri', 'current_funding',
            'heritage_value', 'sustainability_score', 'sdg_alignment'
        ]


class NFTHistorySerializer(serializers.Serializer):
    """Serializer for appending history to NFT"""
    action = serializers.CharField(max_length=100)
    details = serializers.JSONField(required=False, default=dict)