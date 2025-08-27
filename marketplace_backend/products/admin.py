from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'product_type', 'category', 'is_physical', 'is_digital', 'is_redeemable', 'created_at']
    list_filter = ['product_type', 'category', 'is_physical', 'is_digital', 'is_redeemable', 'is_license_based']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'product_type', 'category', 'description')
        }),
        ('Product Properties', {
            'fields': ('is_physical', 'is_digital', 'has_digital_scan', 'is_redeemable', 'is_license_based')
        }),
        ('Media', {
            'fields': ('image', 'digital_file')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('nfts')