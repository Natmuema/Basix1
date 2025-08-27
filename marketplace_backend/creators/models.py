from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Creator(models.Model):
    """
    Represents a creator in the marketplace.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    wallet_address = models.CharField(max_length=100, unique=True)
    skills = models.JSONField(default=list, help_text="List of skills")
    reputation_score = models.IntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Reputation score from 0 to 100"
    )
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='creators/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-reputation_score', '-created_at']
        
    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.wallet_address[:10]}..."
    
    @property
    def is_verified_creator(self):
        """Check if creator has minted at least 1 NFT"""
        return self.nfts_created.exists()
    
    @property
    def total_nfts_created(self):
        return self.nfts_created.count()