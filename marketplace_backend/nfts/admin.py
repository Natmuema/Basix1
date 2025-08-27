from django.contrib import admin
from .models import NFT, Ownership, Utility, GovernanceVote


class OwnershipInline(admin.TabularInline):
    model = Ownership
    extra = 1
    fields = ['creator', 'percentage', 'transfer_rule', 'decay_rule']


class UtilityInline(admin.TabularInline):
    model = Utility
    extra = 1
    fields = ['utility_type', 'description', 'ownership_requirement', 'condition', 'is_active']


class GovernanceVoteInline(admin.TabularInline):
    model = GovernanceVote
    extra = 0
    fields = ['creator', 'weight', 'is_reputation_weighted']
    readonly_fields = ['effective_weight']


@admin.register(NFT)
class NFTAdmin(admin.ModelAdmin):
    list_display = ['id', 'token_id', 'name', 'product', 'is_funded', 'funding_percentage', 'impact_score_display', 'created_at']
    list_filter = ['product__product_type', 'created_at']
    search_fields = ['token_id', 'name', 'product__name']
    readonly_fields = ['created_at', 'updated_at', 'is_funded', 'funding_percentage', 'impact_score_display']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('token_id', 'name', 'product')
        }),
        ('Blockchain Data', {
            'fields': ('contract_address', 'metadata_uri')
        }),
        ('Funding', {
            'fields': ('funding_threshold', 'current_funding', 'is_funded', 'funding_percentage')
        }),
        ('Impact Scoring', {
            'fields': ('heritage_value', 'sustainability_score', 'sdg_alignment', 'impact_score_display')
        }),
        ('History', {
            'fields': ('history',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [OwnershipInline, UtilityInline, GovernanceVoteInline]
    
    def impact_score_display(self, obj):
        return f"{obj.impact_score:.2f}"
    impact_score_display.short_description = 'Impact Score'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('product').prefetch_related('ownerships', 'utilities', 'governance_votes')


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ['id', 'nft', 'creator', 'percentage', 'created_at']
    list_filter = ['created_at']
    search_fields = ['nft__name', 'creator__user__username', 'creator__wallet_address']
    
    fieldsets = (
        ('Ownership Details', {
            'fields': ('nft', 'creator', 'percentage')
        }),
        ('Dynamic Rules', {
            'fields': ('transfer_rule', 'decay_rule'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Utility)
class UtilityAdmin(admin.ModelAdmin):
    list_display = ['id', 'nft', 'utility_type', 'ownership_requirement', 'is_active', 'created_at']
    list_filter = ['utility_type', 'is_active', 'created_at']
    search_fields = ['nft__name', 'description']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('nft', 'utility_type', 'description')
        }),
        ('Access Control', {
            'fields': ('ownership_requirement', 'condition', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )


@admin.register(GovernanceVote)
class GovernanceVoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nft', 'creator', 'weight', 'is_reputation_weighted', 'effective_weight_display', 'created_at']
    list_filter = ['is_reputation_weighted', 'created_at']
    search_fields = ['nft__name', 'creator__user__username']
    readonly_fields = ['effective_weight_display']
    
    fieldsets = (
        ('Vote Details', {
            'fields': ('nft', 'creator', 'weight', 'is_reputation_weighted', 'effective_weight_display')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def effective_weight_display(self, obj):
        return f"{obj.effective_weight:.4f}"
    effective_weight_display.short_description = 'Effective Weight'