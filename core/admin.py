from django.contrib import admin

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


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "wallet_address", "reputation_score", "created_at")
    search_fields = ("name", "wallet_address")
    list_filter = ("reputation_score",)
    filter_horizontal = ("skills",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "category", "physical", "digital", "redeemable")
    search_fields = ("name", "type", "category")
    list_filter = ("type", "category", "physical", "digital", "redeemable")


@admin.register(Utility)
class UtilityAdmin(admin.ModelAdmin):
    list_display = ("id", "code")
    search_fields = ("code",)


@admin.register(NFT)
class NFTAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "product", "created_at")
    search_fields = ("code",)
    list_filter = ("product__type",)
    filter_horizontal = ("utilities",)


@admin.register(NFTOwnership)
class NFTOwnershipAdmin(admin.ModelAdmin):
    list_display = ("id", "nft", "creator", "percentage", "created_at")
    search_fields = ("nft__code", "creator__name")
    list_filter = ("creator",)


@admin.register(DynamicOwnershipRule)
class DynamicOwnershipRuleAdmin(admin.ModelAdmin):
    list_display = ("id", "nft", "creator", "rule_type")
    list_filter = ("rule_type",)
    search_fields = ("nft__code", "creator__name", "rule_text")


@admin.register(GovernanceVote)
class GovernanceVoteAdmin(admin.ModelAdmin):
    list_display = ("id", "nft", "creator", "weight", "reputation_weighted")
    list_filter = ("reputation_weighted",)
    search_fields = ("nft__code", "creator__name")


@admin.register(SDGTag)
class SDGTagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(ImpactScore)
class ImpactScoreAdmin(admin.ModelAdmin):
    list_display = ("id", "nft", "heritage_value", "sustainability_score")
    list_filter = ("heritage_value", "sustainability_score")


@admin.register(FundingThreshold)
class FundingThresholdAdmin(admin.ModelAdmin):
    list_display = ("id", "nft", "amount")
    list_filter = ("nft",)


@admin.register(UtilityGate)
class UtilityGateAdmin(admin.ModelAdmin):
    list_display = ("id", "nft", "utility", "condition")
    list_filter = ("utility",)


@admin.register(NFTActionHistory)
class NFTActionHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "nft", "action", "created_at")
    search_fields = ("nft__code", "action")

