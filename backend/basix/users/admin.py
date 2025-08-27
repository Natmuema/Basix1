from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, CreatorProfile, InvestorProfile, UserVerification, UserSession


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin"""
    list_display = [
        'username', 'email', 'first_name', 'last_name', 'user_type',
        'wallet_address', 'is_verified', 'is_active', 'date_joined'
    ]
    list_filter = [
        'user_type', 'is_verified', 'is_active', 'is_staff', 'is_superuser',
        'date_joined', 'created_at'
    ]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'wallet_address']
    ordering = ['-date_joined']
    readonly_fields = ['created_at', 'updated_at', 'wallet_address']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': (
                'first_name', 'last_name', 'email', 'user_type',
                'wallet_address', 'profile_image', 'bio', 'phone_number',
                'date_of_birth', 'is_verified'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups',
                'user_permissions'
            ),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'first_name', 'last_name', 'user_type'
            ),
        }),
    )


@admin.register(CreatorProfile)
class CreatorProfileAdmin(admin.ModelAdmin):
    """Creator Profile admin"""
    list_display = [
        'user', 'reputation_score', 'experience_years',
        'skills_display', 'specializations_display'
    ]
    list_filter = ['reputation_score', 'experience_years']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['id']
    
    def skills_display(self, obj):
        return ', '.join(obj.skills) if obj.skills else 'No skills'
    skills_display.short_description = 'Skills'
    
    def specializations_display(self, obj):
        return ', '.join(obj.specializations) if obj.specializations else 'No specializations'
    specializations_display.short_description = 'Specializations'


@admin.register(InvestorProfile)
class InvestorProfileAdmin(admin.ModelAdmin):
    """Investor Profile admin"""
    list_display = [
        'user', 'risk_tolerance', 'investment_budget',
        'preferences_display', 'categories_display'
    ]
    list_filter = ['risk_tolerance', 'investment_budget']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['id']
    
    def preferences_display(self, obj):
        return ', '.join(obj.investment_preferences) if obj.investment_preferences else 'No preferences'
    preferences_display.short_description = 'Investment Preferences'
    
    def categories_display(self, obj):
        return ', '.join(obj.preferred_categories) if obj.preferred_categories else 'No categories'
    categories_display.short_description = 'Preferred Categories'


@admin.register(UserVerification)
class UserVerificationAdmin(admin.ModelAdmin):
    """User Verification admin"""
    list_display = [
        'user', 'email_verified', 'phone_verified', 'kyc_completed',
        'email_verification_sent_at', 'phone_verification_sent_at'
    ]
    list_filter = ['email_verified', 'phone_verified', 'kyc_completed']
    search_fields = ['user__username', 'user__email']
    readonly_fields = [
        'id', 'email_verification_token', 'phone_verification_code',
        'email_verification_sent_at', 'phone_verification_sent_at'
    ]


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """User Session admin"""
    list_display = [
        'user', 'ip_address', 'is_active', 'created_at', 'last_activity'
    ]
    list_filter = ['is_active', 'created_at', 'last_activity']
    search_fields = ['user__username', 'ip_address', 'session_key']
    readonly_fields = ['id', 'session_key', 'user_agent', 'created_at', 'last_activity']


# Customize admin site
admin.site.site_header = "BASIX IP Marketplace Admin"
admin.site.site_title = "BASIX Admin Portal"
admin.site.index_title = "Welcome to BASIX IP Marketplace Administration"
