from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Creator, Product, NFT, Utility, Ownership, DynamicOwnership,
    GovernanceVote, UtilityGate, ImpactScore, FundingThreshold,
    NFTHistory, SmartFunction, CreatorStats, MarketplaceConfig
)


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ['user', 'wallet_address', 'reputation_score', 'skills_display', 'created_at']
    list_filter = ['reputation_score', 'created_at']
    search_fields = ['user__username', 'user__email', 'wallet_address']
    readonly_fields = ['created_at', 'updated_at']
    
    def skills_display(self, obj):
        return ', '.join(obj.skills) if obj.skills else 'No skills'
    skills_display.short_description = 'Skills'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_type', 'category', 'creator', 'price', 'is_physical', 'is_digital', 'created_at']
    list_filter = ['product_type', 'category', 'is_physical', 'is_digital', 'is_redeemable', 'created_at']
    search_fields = ['name', 'description', 'creator__user__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    filter_horizontal = []


@admin.register(NFT)
class NFTAdmin(admin.ModelAdmin):
    list_display = ['token_id', 'product_name', 'blockchain_address', 'created_at']
    list_filter = ['created_at', 'product__product_type']
    search_fields = ['token_id', 'product__name', 'blockchain_address']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = 'Product'


@admin.register(Utility)
class UtilityAdmin(admin.ModelAdmin):
    list_display = ['nft', 'utility_type', 'is_active', 'created_at']
    list_filter = ['utility_type', 'is_active', 'created_at']
    search_fields = ['nft__token_id', 'nft__product__name']
    readonly_fields = ['created_at']


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ['nft', 'owner', 'percentage', 'acquired_at']
    list_filter = ['acquired_at', 'updated_at']
    search_fields = ['nft__token_id', 'owner__user__username']
    readonly_fields = ['acquired_at', 'updated_at']


@admin.register(DynamicOwnership)
class DynamicOwnershipAdmin(admin.ModelAdmin):
    list_display = ['nft', 'rule_type', 'is_active', 'created_at']
    list_filter = ['rule_type', 'is_active', 'created_at']
    search_fields = ['nft__token_id', 'rule_description']
    readonly_fields = ['created_at']


@admin.register(GovernanceVote)
class GovernanceVoteAdmin(admin.ModelAdmin):
    list_display = ['nft', 'voter', 'weight', 'is_reputation_weighted', 'created_at']
    list_filter = ['is_reputation_weighted', 'created_at']
    search_fields = ['nft__token_id', 'voter__user__username']
    readonly_fields = ['created_at']


@admin.register(UtilityGate)
class UtilityGateAdmin(admin.ModelAdmin):
    list_display = ['nft', 'utility', 'condition', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['nft__token_id', 'utility__utility_type']
    readonly_fields = ['created_at']


@admin.register(ImpactScore)
class ImpactScoreAdmin(admin.ModelAdmin):
    list_display = ['nft', 'heritage_value', 'sustainability_score', 'sdg_alignment_display', 'calculated_at']
    list_filter = ['heritage_value', 'sustainability_score', 'calculated_at']
    search_fields = ['nft__token_id', 'nft__product__name']
    readonly_fields = ['calculated_at']
    
    def sdg_alignment_display(self, obj):
        return ', '.join(obj.sdg_alignment) if obj.sdg_alignment else 'No SDG alignment'
    sdg_alignment_display.short_description = 'SDG Alignment'


@admin.register(FundingThreshold)
class FundingThresholdAdmin(admin.ModelAdmin):
    list_display = ['nft', 'amount', 'currency', 'is_met', 'created_at']
    list_filter = ['is_met', 'currency', 'created_at']
    search_fields = ['nft__token_id', 'nft__product__name']
    readonly_fields = ['created_at', 'met_at']


@admin.register(NFTHistory)
class NFTHistoryAdmin(admin.ModelAdmin):
    list_display = ['nft', 'action_type', 'performed_by', 'timestamp']
    list_filter = ['action_type', 'timestamp']
    search_fields = ['nft__token_id', 'performed_by__user__username']
    readonly_fields = ['timestamp']


@admin.register(SmartFunction)
class SmartFunctionAdmin(admin.ModelAdmin):
    list_display = ['name', 'function_type', 'is_active', 'created_at']
    list_filter = ['function_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']


@admin.register(CreatorStats)
class CreatorStatsAdmin(admin.ModelAdmin):
    list_display = ['creator', 'total_nfts_created', 'total_sales', 'total_royalties_earned', 'average_rating', 'last_updated']
    list_filter = ['last_updated']
    search_fields = ['creator__user__username']
    readonly_fields = ['last_updated']


@admin.register(MarketplaceConfig)
class MarketplaceConfigAdmin(admin.ModelAdmin):
    list_display = ['key', 'value_display', 'is_active', 'updated_at']
    list_filter = ['is_active', 'updated_at']
    search_fields = ['key', 'description']
    readonly_fields = ['updated_at']
    
    def value_display(self, obj):
        if isinstance(obj.value, dict):
            return format_html('<pre>{}</pre>', str(obj.value))
        return str(obj.value)
    value_display.short_description = 'Value'


# Custom admin site configuration
admin.site.site_header = "Marketplace Knowledge Base Admin"
admin.site.site_title = "Marketplace Admin Portal"
admin.site.index_title = "Welcome to Marketplace Knowledge Base Administration"