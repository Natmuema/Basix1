from django.contrib import admin
from .models import (
    Creator, Product, NFT, Utility, Ownership, DynamicOwnership,
    GovernanceVote, UtilityGate, ImpactScore, FundingThreshold,
    NFTHistory, MarketplaceStats
)


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ['user', 'wallet_address', 'reputation_score', 'created_at']
    list_filter = ['reputation_score', 'created_at']
    search_fields = ['user__username', 'user__email', 'wallet_address']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_type', 'category', 'creator', 'created_at']
    list_filter = ['product_type', 'category', 'is_physical', 'is_digital', 'created_at']
    search_fields = ['name', 'description', 'creator__user__username']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(NFT)
class NFTAdmin(admin.ModelAdmin):
    list_display = ['token_id', 'product', 'creator', 'is_minted', 'is_listed']
    list_filter = ['is_minted', 'is_listed', 'blockchain', 'created_at']
    search_fields = ['token_id', 'product__name', 'creator__user__username']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Utility)
class UtilityAdmin(admin.ModelAdmin):
    list_display = ['nft', 'utility_type', 'is_active']
    list_filter = ['utility_type', 'is_active']
    search_fields = ['nft__token_id', 'nft__product__name']


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ['nft', 'creator', 'percentage', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['nft__token_id', 'creator__user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(DynamicOwnership)
class DynamicOwnershipAdmin(admin.ModelAdmin):
    list_display = ['nft', 'rule_type', 'is_active']
    list_filter = ['rule_type', 'is_active', 'created_at']
    search_fields = ['nft__token_id', 'rule_description']


@admin.register(GovernanceVote)
class GovernanceVoteAdmin(admin.ModelAdmin):
    list_display = ['nft', 'creator', 'weight', 'is_reputation_weighted']
    list_filter = ['is_reputation_weighted', 'vote_timestamp']
    search_fields = ['nft__token_id', 'creator__user__username']


@admin.register(UtilityGate)
class UtilityGateAdmin(admin.ModelAdmin):
    list_display = ['nft', 'utility', 'condition', 'is_active']
    list_filter = ['is_active']
    search_fields = ['nft__token_id', 'utility__utility_type']


@admin.register(ImpactScore)
class ImpactScoreAdmin(admin.ModelAdmin):
    list_display = ['nft', 'heritage_value', 'sustainability_score', 'calculated_at']
    list_filter = ['heritage_value', 'sustainability_score', 'calculated_at']
    search_fields = ['nft__token_id', 'nft__product__name']


@admin.register(FundingThreshold)
class FundingThresholdAdmin(admin.ModelAdmin):
    list_display = ['nft', 'amount', 'currency', 'is_active']
    list_filter = ['currency', 'is_active', 'created_at']
    search_fields = ['nft__token_id', 'nft__product__name']


@admin.register(NFTHistory)
class NFTHistoryAdmin(admin.ModelAdmin):
    list_display = ['nft', 'action_type', 'user', 'timestamp']
    list_filter = ['action_type', 'timestamp']
    search_fields = ['nft__token_id', 'action_description', 'user__username']
    readonly_fields = ['timestamp']


@admin.register(MarketplaceStats)
class MarketplaceStatsAdmin(admin.ModelAdmin):
    list_display = ['total_nfts', 'total_creators', 'total_volume', 'active_listings', 'last_updated']
    readonly_fields = ['last_updated']