from django.contrib import admin
from .models import Creator


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'wallet_address', 'reputation_score', 'is_verified_creator', 'created_at']
    list_filter = ['reputation_score', 'created_at']
    search_fields = ['user__username', 'wallet_address', 'bio']
    readonly_fields = ['created_at', 'updated_at', 'is_verified_creator', 'total_nfts_created']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'wallet_address', 'bio', 'profile_image')
        }),
        ('Skills & Reputation', {
            'fields': ('skills', 'reputation_score')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('is_verified_creator', 'total_nfts_created'),
            'classes': ('collapse',)
        })
    )
    
    def is_verified_creator(self, obj):
        return obj.is_verified_creator
    is_verified_creator.boolean = True
    is_verified_creator.short_description = 'Verified Creator'
    
    def total_nfts_created(self, obj):
        return obj.total_nfts_created
    total_nfts_created.short_description = 'Total NFTs Created'