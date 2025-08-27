from django.contrib import admin
from .models import Transaction, ImpactMetrics, MarketplaceStats


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'transaction_type', 'nft', 'from_creator', 'to_creator', 'amount', 'timestamp']
    list_filter = ['transaction_type', 'timestamp']
    search_fields = ['nft__name', 'transaction_hash', 'from_creator__user__username', 'to_creator__user__username']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('transaction_type', 'nft', 'from_creator', 'to_creator')
        }),
        ('Financial Details', {
            'fields': ('amount', 'ownership_percentage')
        }),
        ('Blockchain Data', {
            'fields': ('transaction_hash', 'block_number'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata', 'timestamp'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('nft', 'from_creator', 'to_creator')


@admin.register(ImpactMetrics)
class ImpactMetricsAdmin(admin.ModelAdmin):
    list_display = ['id', 'nft', 'overall_impact_score', 'heritage_value', 'sustainability_score', 'total_funding', 'recorded_at']
    list_filter = ['recorded_at']
    search_fields = ['nft__name']
    readonly_fields = ['recorded_at']
    date_hierarchy = 'recorded_at'
    
    fieldsets = (
        ('NFT', {
            'fields': ('nft',)
        }),
        ('Impact Scores', {
            'fields': ('heritage_value', 'sustainability_score', 'overall_impact_score')
        }),
        ('Community Metrics', {
            'fields': ('total_supporters', 'total_funding')
        }),
        ('Activity Metrics', {
            'fields': ('transactions_count', 'utilities_redeemed')
        }),
        ('Timestamp', {
            'fields': ('recorded_at',),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('nft')


@admin.register(MarketplaceStats)
class MarketplaceStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_creators', 'verified_creators', 'total_nfts', 'funded_nfts', 'daily_transactions', 'daily_volume']
    list_filter = ['date']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Date', {
            'fields': ('date',)
        }),
        ('Creator Statistics', {
            'fields': ('total_creators', 'verified_creators', 'average_reputation')
        }),
        ('NFT Statistics', {
            'fields': ('total_nfts', 'funded_nfts', 'total_funding_raised')
        }),
        ('Product Statistics', {
            'fields': ('total_products', 'products_by_type')
        }),
        ('Transaction Statistics', {
            'fields': ('daily_transactions', 'daily_volume')
        }),
        ('Impact Statistics', {
            'fields': ('average_heritage_value', 'average_sustainability_score')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        # Stats should be generated automatically, not added manually
        return False