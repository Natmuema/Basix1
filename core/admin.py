from django.contrib import admin

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


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ("name", "wallet", "reputation_score", "is_creator")
    search_fields = ("name", "wallet")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "category", "physical", "digital", "redeemable")
    list_filter = ("type", "category", "physical", "digital", "redeemable")
    search_fields = ("name", "category")


class NFTEventInline(admin.TabularInline):
    model = NFTEvent
    extra = 0


@admin.register(NFT)
class NFTAdmin(admin.ModelAdmin):
    list_display = ("code", "product")
    search_fields = ("code",)
    inlines = [NFTEventInline]


@admin.register(NFTUtility)
class NFTUtilityAdmin(admin.ModelAdmin):
    list_display = ("nft", "utility_type")
    list_filter = ("utility_type",)


@admin.register(UtilityGate)
class UtilityGateAdmin(admin.ModelAdmin):
    list_display = ("nft_utility", "condition")


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ("nft", "creator", "percentage")
    list_filter = ("nft", "creator")


@admin.register(DynamicOwnershipRule)
class DynamicOwnershipRuleAdmin(admin.ModelAdmin):
    list_display = ("nft", "rule_type", "description")
    list_filter = ("rule_type",)


@admin.register(GovernanceVote)
class GovernanceVoteAdmin(admin.ModelAdmin):
    list_display = ("nft", "creator", "weight", "reputation_weighted")
    list_filter = ("reputation_weighted",)


@admin.register(ImpactScore)
class ImpactScoreAdmin(admin.ModelAdmin):
    list_display = ("nft", "heritage_value", "sustainability_score", "computed_value")


@admin.register(FundingThreshold)
class FundingThresholdAdmin(admin.ModelAdmin):
    list_display = ("nft", "amount")


# Register your models here.
