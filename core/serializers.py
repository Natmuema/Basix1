from rest_framework import serializers

from .models import (
    Skill,
    Creator,
    Product,
    Utility,
    NFT,
    NFTOwnership,
    DynamicOwnershipRule,
    GovernanceVote,
    SDGTag,
    ImpactScore,
    FundingThreshold,
    UtilityGate,
    NFTActionHistory,
)


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class CreatorSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True, required=False)
    is_creator = serializers.BooleanField(read_only=True)

    class Meta:
        model = Creator
        fields = [
            "id",
            "name",
            "wallet_address",
            "reputation_score",
            "skills",
            "is_creator",
            "created_at",
            "updated_at",
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
            "created_at",
            "updated_at",
        ]


class UtilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Utility
        fields = ["id", "code"]


class NFTSerializer(serializers.ModelSerializer):
    utilities = serializers.PrimaryKeyRelatedField(queryset=Utility.objects.all(), many=True, required=False)

    class Meta:
        model = NFT
        fields = ["id", "code", "product", "utilities", "created_at", "updated_at"]


class NFTOwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTOwnership
        fields = ["id", "nft", "creator", "percentage", "created_at", "updated_at"]


class DynamicOwnershipRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicOwnershipRule
        fields = ["id", "nft", "creator", "rule_type", "rule_text", "created_at", "updated_at"]


class GovernanceVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernanceVote
        fields = ["id", "nft", "creator", "weight", "reputation_weighted", "created_at", "updated_at"]


class SDGTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SDGTag
        fields = ["id", "name"]


class ImpactScoreSerializer(serializers.ModelSerializer):
    sdg_alignment = serializers.PrimaryKeyRelatedField(queryset=SDGTag.objects.all(), many=True, required=False)

    class Meta:
        model = ImpactScore
        fields = ["id", "nft", "heritage_value", "sustainability_score", "sdg_alignment", "created_at", "updated_at"]


class FundingThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundingThreshold
        fields = ["id", "nft", "amount", "created_at", "updated_at"]


class UtilityGateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityGate
        fields = ["id", "nft", "utility", "condition", "created_at", "updated_at"]


class NFTActionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTActionHistory
        fields = ["id", "nft", "action", "created_at", "updated_at"]

