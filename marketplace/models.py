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
    """Product model representing various types of creative and cultural products"""
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
        ('Safari', 'Safari'),
        ('Oral_History', 'Oral History'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    category = models.CharField(max_length=20, choices=CATEGORIES, blank=True)
    description = models.TextField()
    
    # Product attributes
    is_physical = models.BooleanField(default=False)
    is_digital = models.BooleanField(default=False)
    is_redeemable = models.BooleanField(default=False)
    has_digital_scan = models.BooleanField(default=False)
    is_license_based = models.BooleanField(default=False)
    
    # Metadata
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional fields
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    tags = models.JSONField(default=list)
    
    def __str__(self):
        return f"{self.name} ({self.product_type})"

    class Meta:
        ordering = ['-created_at']


class NFT(models.Model):
    """NFT model representing blockchain-based digital assets"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token_id = models.CharField(max_length=255, unique=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='nft')
    blockchain_address = models.CharField(max_length=255)
    contract_address = models.CharField(max_length=255)
    metadata_uri = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"NFT {self.token_id} - {self.product.name}"

    class Meta:
        ordering = ['-created_at']


class Utility(models.Model):
    """Utility model representing various utilities associated with NFTs"""
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
    utility_type = models.CharField(max_length=30, choices=UTILITY_TYPES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nft.token_id} - {self.utility_type}"

    class Meta:
        unique_together = ['nft', 'utility_type']


class Ownership(models.Model):
    """Ownership model representing fractional ownership of NFTs"""
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name='ownerships')
    owner = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='owned_nfts')
    percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    acquired_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.owner.user.username} owns {self.percentage}% of {self.nft.token_id}"

    class Meta:
        unique_together = ['nft', 'owner']


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
    voter = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='votes_cast')
    weight = models.DecimalField(max_digits=3, decimal_places=2, default=1.00)
    is_reputation_weighted = models.BooleanField(default=True)
    vote_data = models.JSONField(default=dict)  # Store vote details
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Vote by {self.voter.user.username} on {self.nft.token_id}"

    class Meta:
        unique_together = ['nft', 'voter']


class UtilityGate(models.Model):
    """Utility gating system for NFT utilities"""
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name='utility_gates')
    utility = models.ForeignKey(Utility, on_delete=models.CASCADE, related_name='gates')
    condition = models.TextField()  # e.g., ">=20% ownership required"
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Gate for {self.utility.utility_type} on {self.nft.token_id}"


class ImpactScore(models.Model):
    """Impact scoring system for NFTs"""
    nft = models.OneToOneField(NFT, on_delete=models.CASCADE, related_name='impact_score')
    heritage_value = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    sustainability_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    sdg_alignment = models.JSONField(default=list)  # ["Tourism", "Wildlife_Protection"]
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Impact score for {self.nft.token_id}: {self.heritage_value}/{self.sustainability_score}"


class FundingThreshold(models.Model):
    """Funding thresholds for NFTs"""
    nft = models.OneToOneField(NFT, on_delete=models.CASCADE, related_name='funding_threshold')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    is_met = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    met_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Funding threshold for {self.nft.token_id}: {self.amount} {self.currency}"


class NFTHistory(models.Model):
    """History tracking for NFT actions"""
    ACTION_TYPES = [
        ('minted', 'Minted'),
        ('sold', 'Sold'),
        ('transferred', 'Transferred'),
        ('utility_used', 'Utility Used'),
        ('governance_vote', 'Governance Vote'),
        ('ownership_changed', 'Ownership Changed'),
        ('funding_met', 'Funding Threshold Met'),
    ]

    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name='history')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    action_data = models.JSONField(default=dict)  # Store action details
    performed_by = models.ForeignKey(Creator, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nft.token_id} - {self.action_type} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']


class SmartFunction(models.Model):
    """Smart functions for NFT operations"""
    FUNCTION_TYPES = [
        ('append_history', 'Append History'),
        ('impact_score', 'Calculate Impact Score'),
        ('is_creator', 'Check Creator Status'),
        ('ownership_calculation', 'Ownership Calculation'),
        ('utility_validation', 'Utility Validation'),
    ]

    name = models.CharField(max_length=100)
    function_type = models.CharField(max_length=30, choices=FUNCTION_TYPES)
    description = models.TextField()
    parameters = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.function_type})"


class CreatorStats(models.Model):
    """Statistics for creators"""
    creator = models.OneToOneField(Creator, on_delete=models.CASCADE, related_name='stats')
    total_nfts_created = models.IntegerField(default=0)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_royalties_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    followers_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Stats for {self.creator.user.username}"


class MarketplaceConfig(models.Model):
    """Global marketplace configuration"""
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.key}: {self.value}"