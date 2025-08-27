from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    USER_TYPE_CHOICES = [
        ('creator', 'Creator'),
        ('investor', 'Investor'),
        ('admin', 'Admin'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='creator')
    wallet_address = models.CharField(max_length=255, unique=True, blank=True)
    profile_image = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.email})"
    
    def save(self, *args, **kwargs):
        if not self.wallet_address:
            self.wallet_address = f"wallet_{uuid.uuid4().hex[:16]}"
        super().save(*args, **kwargs)


class CreatorProfile(models.Model):
    """Extended profile for creators"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='creator_profile')
    skills = models.JSONField(default=list)
    reputation_score = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    portfolio_url = models.URLField(blank=True)
    social_media_links = models.JSONField(default=dict)
    specializations = models.JSONField(default=list)
    experience_years = models.IntegerField(default=0)
    awards = models.JSONField(default=list)
    
    class Meta:
        db_table = 'users_creator_profile'
    
    def __str__(self):
        return f"Creator Profile: {self.user.username}"


class InvestorProfile(models.Model):
    """Extended profile for investors"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='investor_profile')
    investment_preferences = models.JSONField(default=list)
    risk_tolerance = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
        ],
        default='medium'
    )
    investment_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    preferred_categories = models.JSONField(default=list)
    investment_history = models.JSONField(default=list)
    
    class Meta:
        db_table = 'users_investor_profile'
    
    def __str__(self):
        return f"Investor Profile: {self.user.username}"


class UserSession(models.Model):
    """Track user sessions for security"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'users_user_session'
    
    def __str__(self):
        return f"Session: {self.user.username} - {self.ip_address}"


class UserVerification(models.Model):
    """User verification and email confirmation"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification')
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True)
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)
    phone_verified = models.BooleanField(default=False)
    phone_verification_code = models.CharField(max_length=6, blank=True)
    phone_verification_sent_at = models.DateTimeField(null=True, blank=True)
    kyc_completed = models.BooleanField(default=False)
    kyc_documents = models.JSONField(default=list)
    
    class Meta:
        db_table = 'users_user_verification'
    
    def __str__(self):
        return f"Verification: {self.user.username}"
