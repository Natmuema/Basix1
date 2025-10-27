from rest_framework import serializers

from .models import (
    Creator,
    Product,
    NFT,
    NFTEvent,
    NFTUtility,
    UtilityGate,
    Ownership,
    DynamicOwnershipRule,
    GovernanceVote,
    ImpactScore,
    FundingThreshold,
)


class CreatorSerializer(serializers.ModelSerializer):
    is_creator = serializers.ReadOnlyField()

    class Meta:
        model = Creator
        fields = [
            "id",
            "name",
            "wallet",
            "skills",
            "reputation_score",
            "is_creator",
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "type",
            "description",
            "category",
            "physical",
            "digital",
            "digital_scan",
            "redeemable",
            "license_based",
        ]


class NFTEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTEvent
        fields = ["id", "action", "created_at"]


class NFTUtilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTUtility
        fields = ["id", "utility_type", "nft"]


class UtilityGateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityGate
        fields = ["id", "condition", "nft_utility"]


class OwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ownership
        fields = ["id", "nft", "creator", "percentage"]


class DynamicOwnershipRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicOwnershipRule
        fields = ["id", "nft", "rule_type", "description"]


class GovernanceVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernanceVote
        fields = ["id", "nft", "creator", "weight", "reputation_weighted"]


class ImpactScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactScore
        fields = [
            "id",
            "nft",
            "heritage_value",
            "sustainability_score",
            "sdg_alignment",
            "computed_value",
        ]


class FundingThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundingThreshold
        fields = ["id", "nft", "amount"]


class NFTSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )
    events = NFTEventSerializer(many=True, read_only=True)
    utilities = NFTUtilitySerializer(many=True, read_only=True)
    impact = ImpactScoreSerializer(read_only=True)
    funding_threshold = FundingThresholdSerializer(read_only=True)

    class Meta:
        model = NFT
        fields = [
            "id",
            "code",
            "product",
            "product_id",
            "events",
            "utilities",
            "impact",
            "funding_threshold",
        ]

