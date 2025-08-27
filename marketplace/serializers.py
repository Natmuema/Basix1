from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Creator, Product, NFT, Utility, Ownership, DynamicOwnership,
    GovernanceVote, UtilityGate, ImpactScore, FundingThreshold,
    NFTHistory, SmartFunction, CreatorStats, MarketplaceConfig
)
from django.core.validators import MinValueValidator, MaxValueValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']


class CreatorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    total_products = serializers.SerializerMethodField()
    total_nfts_owned = serializers.SerializerMethodField()

    class Meta:
        model = Creator
        fields = [
            'id', 'user', 'wallet_address', 'skills', 'reputation_score',
            'bio', 'profile_image', 'created_at', 'updated_at',
            'total_products', 'total_nfts_owned'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_total_products(self, obj):
        return obj.products.count()

    def get_total_nfts_owned(self, obj):
        return obj.owned_nfts.count()


class CreatorStatsSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer(read_only=True)

    class Meta:
        model = CreatorStats
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer(read_only=True)
    creator_id = serializers.PrimaryKeyRelatedField(
        queryset=Creator.objects.all(),
        source='creator',
        write_only=True
    )
    has_nft = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'product_type', 'category', 'description',
            'is_physical', 'is_digital', 'is_redeemable', 'has_digital_scan',
            'is_license_based', 'creator', 'creator_id', 'created_at',
            'updated_at', 'price', 'currency', 'tags', 'has_nft'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_has_nft(self, obj):
        return hasattr(obj, 'nft')


class NFTSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    utilities = serializers.SerializerMethodField()
    ownerships = serializers.SerializerMethodField()
    impact_score = serializers.SerializerMethodField()
    funding_threshold = serializers.SerializerMethodField()

    class Meta:
        model = NFT
        fields = [
            'id', 'token_id', 'product', 'product_id', 'blockchain_address',
            'contract_address', 'metadata_uri', 'created_at', 'updated_at',
            'utilities', 'ownerships', 'impact_score', 'funding_threshold'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_utilities(self, obj):
        return UtilitySerializer(obj.utilities.all(), many=True).data

    def get_ownerships(self, obj):
        return OwnershipSerializer(obj.ownerships.all(), many=True).data

    def get_impact_score(self, obj):
        if hasattr(obj, 'impact_score'):
            return ImpactScoreSerializer(obj.impact_score).data
        return None

    def get_funding_threshold(self, obj):
        if hasattr(obj, 'funding_threshold'):
            return FundingThresholdSerializer(obj.funding_threshold).data
        return None


class UtilitySerializer(serializers.ModelSerializer):
    nft = NFTSerializer(read_only=True)
    nft_id = serializers.PrimaryKeyRelatedField(
        queryset=NFT.objects.all(),
        source='nft',
        write_only=True
    )

    class Meta:
        model = Utility
        fields = [
            'id', 'nft', 'nft_id', 'utility_type', 'description',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class OwnershipSerializer(serializers.ModelSerializer):
    nft = NFTSerializer(read_only=True)
    owner = CreatorSerializer(read_only=True)
    nft_id = serializers.PrimaryKeyRelatedField(
        queryset=NFT.objects.all(),
        source='nft',
        write_only=True
    )
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=Creator.objects.all(),
        source='owner',
        write_only=True
    )

    class Meta:
        model = Ownership
        fields = [
            'id', 'nft', 'nft_id', 'owner', 'owner_id', 'percentage',
            'acquired_at', 'updated_at'
        ]
        read_only_fields = ['id', 'acquired_at', 'updated_at']


class DynamicOwnershipSerializer(serializers.ModelSerializer):
    nft = NFTSerializer(read_only=True)
    nft_id = serializers.PrimaryKeyRelatedField(
        queryset=NFT.objects.all(),
        source='nft',
        write_only=True
    )

    class Meta:
        model = DynamicOwnership
        fields = [
            'id', 'nft', 'nft_id', 'rule_type', 'rule_description',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class GovernanceVoteSerializer(serializers.ModelSerializer):
    nft = NFTSerializer(read_only=True)
    voter = CreatorSerializer(read_only=True)
    nft_id = serializers.PrimaryKeyRelatedField(
        queryset=NFT.objects.all(),
        source='nft',
        write_only=True
    )
    voter_id = serializers.PrimaryKeyRelatedField(
        queryset=Creator.objects.all(),
        source='voter',
        write_only=True
    )

    class Meta:
        model = GovernanceVote
        fields = [
            'id', 'nft', 'nft_id', 'voter', 'voter_id', 'weight',
            'is_reputation_weighted', 'vote_data', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UtilityGateSerializer(serializers.ModelSerializer):
    nft = NFTSerializer(read_only=True)
    utility = UtilitySerializer(read_only=True)
    nft_id = serializers.PrimaryKeyRelatedField(
        queryset=NFT.objects.all(),
        source='nft',
        write_only=True
    )
    utility_id = serializers.PrimaryKeyRelatedField(
        queryset=Utility.objects.all(),
        source='utility',
        write_only=True
    )

    class Meta:
        model = UtilityGate
        fields = [
            'id', 'nft', 'nft_id', 'utility', 'utility_id', 'condition',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ImpactScoreSerializer(serializers.ModelSerializer):
    nft = NFTSerializer(read_only=True)
    nft_id = serializers.PrimaryKeyRelatedField(
        queryset=NFT.objects.all(),
        source='nft',
        write_only=True
    )

    class Meta:
        model = ImpactScore
        fields = [
            'id', 'nft', 'nft_id', 'heritage_value', 'sustainability_score',
            'sdg_alignment', 'calculated_at'
        ]
        read_only_fields = ['id', 'calculated_at']


class FundingThresholdSerializer(serializers.ModelSerializer):
    nft = NFTSerializer(read_only=True)
    nft_id = serializers.PrimaryKeyRelatedField(
        queryset=NFT.objects.all(),
        source='nft',
        write_only=True
    )

    class Meta:
        model = FundingThreshold
        fields = [
            'id', 'nft', 'nft_id', 'amount', 'currency', 'is_met',
            'created_at', 'met_at'
        ]
        read_only_fields = ['id', 'created_at', 'met_at']


class NFTHistorySerializer(serializers.ModelSerializer):
    nft = NFTSerializer(read_only=True)
    performed_by = CreatorSerializer(read_only=True)
    nft_id = serializers.PrimaryKeyRelatedField(
        queryset=NFT.objects.all(),
        source='nft',
        write_only=True
    )
    performed_by_id = serializers.PrimaryKeyRelatedField(
        queryset=Creator.objects.all(),
        source='performed_by',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = NFTHistory
        fields = [
            'id', 'nft', 'nft_id', 'action_type', 'action_data',
            'performed_by', 'performed_by_id', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']


class SmartFunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartFunction
        fields = [
            'id', 'name', 'function_type', 'description', 'parameters',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class MarketplaceConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceConfig
        fields = [
            'id', 'key', 'value', 'description', 'is_active', 'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']


# Nested serializers for detailed views
class DetailedNFTSerializer(NFTSerializer):
    utilities = UtilitySerializer(many=True, read_only=True)
    ownerships = OwnershipSerializer(many=True, read_only=True)
    governance_votes = GovernanceVoteSerializer(many=True, read_only=True)
    utility_gates = UtilityGateSerializer(many=True, read_only=True)
    dynamic_ownership_rules = DynamicOwnershipSerializer(many=True, read_only=True)
    history = NFTHistorySerializer(many=True, read_only=True)

    class Meta(NFTSerializer.Meta):
        fields = NFTSerializer.Meta.fields + [
            'governance_votes', 'utility_gates', 'dynamic_ownership_rules', 'history'
        ]


class DetailedCreatorSerializer(CreatorSerializer):
    products = ProductSerializer(many=True, read_only=True)
    owned_nfts = OwnershipSerializer(many=True, read_only=True)
    votes_cast = GovernanceVoteSerializer(many=True, read_only=True)
    stats = CreatorStatsSerializer(read_only=True)

    class Meta(CreatorSerializer.Meta):
        fields = CreatorSerializer.Meta.fields + [
            'products', 'owned_nfts', 'votes_cast', 'stats'
        ]


# Specialized serializers for specific operations
class NFTCreationSerializer(serializers.ModelSerializer):
    product_data = ProductSerializer(write_only=True)
    utilities = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    initial_ownership = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100.00
    )

    class Meta:
        model = NFT
        fields = [
            'token_id', 'blockchain_address', 'contract_address',
            'metadata_uri', 'product_data', 'utilities', 'initial_ownership'
        ]

    def create(self, validated_data):
        product_data = validated_data.pop('product_data')
        utilities = validated_data.pop('utilities', [])
        initial_ownership = validated_data.pop('initial_ownership', 100.00)

        # Create product first
        product = Product.objects.create(**product_data)
        
        # Create NFT
        nft = NFT.objects.create(product=product, **validated_data)
        
        # Create utilities
        for utility_type in utilities:
            Utility.objects.create(nft=nft, utility_type=utility_type)
        
        # Create initial ownership
        if initial_ownership > 0:
            Ownership.objects.create(
                nft=nft,
                owner=product.creator,
                percentage=initial_ownership
            )
        
        return nft


class OwnershipTransferSerializer(serializers.Serializer):
    from_owner_id = serializers.PrimaryKeyRelatedField(queryset=Creator.objects.all())
    to_owner_id = serializers.PrimaryKeyRelatedField(queryset=Creator.objects.all())
    nft_id = serializers.PrimaryKeyRelatedField(queryset=NFT.objects.all())
    percentage = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )


class ImpactScoreCalculationSerializer(serializers.Serializer):
    nft_id = serializers.PrimaryKeyRelatedField(queryset=NFT.objects.all())
    heritage_value = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    sustainability_score = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    sdg_alignment = serializers.ListField(child=serializers.CharField())