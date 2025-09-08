from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Creator(models.Model):
    """Creator model representing artists, developers, and content creators"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='creator_profile')
    wallet_address = models.CharField(max_length=255, unique=True)
    skills = models.JSONField(default=list)  # ["art", "beadwork", "music", etc.]
    reputation_score = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    bio = models.TextField(blank=True)
    profile_image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.wallet_address})"

    class Meta:
        ordering = ['-reputation_score']


class Product(models.Model):
    """Product model representing various types of products"""
    PRODUCT_TYPES = [
        ('ArtCraft', 'Art & Craft'),
        ('Music', 'Music'),
        ('Fashion', 'Fashion'),
        ('Tourism', 'Tourism'),
        ('Heritage', 'Heritage'),
        ('Software', 'Software'),
    ]

    CATEGORIES = [
        ('Beadwork', 'Beadwork'),
        ('Afrobeat', 'Afrobeat'),
        ('Textile', 'Textile'),
        ('AI/ML', 'AI/ML'),
        ('Gaming', 'Gaming'),
        ('EcoTourism', 'Eco Tourism'),
        ('OralHistory', 'Oral History'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPES)
    category = models.CharField(max_length=50, choices=CATEGORIES, blank=True)
    description = models.TextField()
    
    # Product attributes
    is_physical = models.BooleanField(default=False)
    is_digital = models.BooleanField(default=False)
    is_redeemable = models.BooleanField(default=False)
    has_digital_scan = models.BooleanField(default=False)
    is_license_based = models.BooleanField(default=False)
    
    # Creator relationship
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='products')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.product_type})"


class NFT(models.Model):
    """NFT model representing digital tokens linked to products"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token_id = models.CharField(max_length=255, unique=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='nft')
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='nfts')
    
    # NFT metadata
    metadata_uri = models.URLField(blank=True)
    blockchain = models.CharField(max_length=50, default='Ethereum')
    contract_address = models.CharField(max_length=255, blank=True)
    
    # Status
    is_minted = models.BooleanField(default=False)
    is_listed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"NFT {self.token_id} - {self.product.name}"


class Utility(models.Model):
    """Utility model representing NFT utilities"""
    UTILITY_TYPES = [
        ('provenance', 'Provenance'),
        ('resale_rights', 'Resale Rights'),
        ('streaming_rights', 'Streaming Rights'),
        ('royalties', 'Royalties'),
        ('redeem_physical', 'Redeem Physical'),
        ('digital_wearable', 'Digital Wearable'),
        ('redeemable_experience', 'Redeemable Experience'),
        ('eco_tourism_support', 'Eco Tourism Support'),
        ('archive_access', 'Archive Access'),
        ('preservation_funding', 'Preservation Funding'),
        ('license_key', 'License Key'),
        ('subscription_access', 'Subscription Access'),
        ('royalty_share', 'Royalty Share'),
        ('lifetime_access', 'Lifetime Access'),
        ('in_game_assets', 'In-Game Assets'),
        ('updates_access', 'Updates Access'),
    ]
    
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name='utilities')
    utility_type = models.CharField(max_length=50, choices=UTILITY_TYPES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nft.token_id} - {self.utility_type}"


class Ownership(models.Model):
    """Ownership model representing fractional ownership of NFTs"""
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name='ownerships')
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='ownerships')
    percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['nft', 'creator']
    
    def __str__(self):
        return f"{self.creator.user.username} owns {self.percentage}% of {self.nft.token_id}"


class DynamicOwnership(models.Model):
    """Dynamic ownership rules for NFTs"""
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name='dynamic_ownership_rules')
    rule_type = models.CharField(max_length=50)  # 'transfer_rule', 'decay_rule', etc.
    rule_description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Dynamic rule for {self.nft.token_id}: {self.rule_type}"


class GovernanceVote(models.Model):
    """Governance voting system for NFTs"""
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name='governance_votes')
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='governance_votes')
    weight = models.DecimalField(max_digits=3, decimal_places=2, default=1.0)
    is_reputation_weighted = models.BooleanField(default=True)
    vote_timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Vote by {self.creator.user.username} on {self.nft.token_id}"


class UtilityGate(models.Model):
    """Utility gating conditions"""
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name='utility_gates')
    utility = models.ForeignKey(Utility, on_delete=models.CASCADE, related_name='gates')
    condition = models.TextField()  # e.g., ">=20% ownership required"
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Gate for {self.utility.utility_type} on {self.nft.token_id}"


class ImpactScore(models.Model):
    """Impact scoring for NFTs"""
    nft = models.OneToOneField(NFT, on_delete=models.CASCADE, related_name='impact_score')
    heritage_value = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    sustainability_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    sdg_alignment = models.JSONField(default=list)  # ["Tourism", "Wildlife_Protection"]
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Impact score for {self.nft.token_id}"


class FundingThreshold(models.Model):
    """Funding thresholds for NFTs"""
    nft = models.OneToOneField(NFT, on_delete=models.CASCADE, related_name='funding_threshold')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Funding threshold: {self.amount} {self.currency} for {self.nft.token_id}"


class NFTHistory(models.Model):
    """NFT transaction and action history"""
    ACTION_TYPES = [
        ('mint', 'Mint'),
        ('sale', 'Sale'),
        ('transfer', 'Transfer'),
        ('upgrade', 'Upgrade'),
        ('stream', 'Stream'),
        ('redeem', 'Redeem'),
        ('vote', 'Vote'),
    ]
    
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name='history')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    action_description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)  # Additional action data
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.nft.token_id} - {self.action_type} at {self.timestamp}"


class MarketplaceStats(models.Model):
    """Marketplace statistics and analytics"""
    total_nfts = models.IntegerField(default=0)
    total_creators = models.IntegerField(default=0)
    total_volume = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    active_listings = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Marketplace Statistics"
    
    def __str__(self):
        return f"Marketplace Stats - {self.last_updated}"