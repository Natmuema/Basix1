from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from creators.models import Creator
from products.models import Product


class NFT(models.Model):
    """
    Represents an NFT that links to a product.
    """
    token_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='nfts')
    
    # Blockchain data
    contract_address = models.CharField(max_length=100, blank=True)
    metadata_uri = models.URLField(blank=True)
    
    # Funding
    funding_threshold = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        help_text="Funding threshold in USD"
    )
    current_funding = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    # Impact scoring
    heritage_value = models.IntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Heritage value score from 0 to 100"
    )
    sustainability_score = models.IntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Sustainability score from 0 to 100"
    )
    sdg_alignment = models.JSONField(
        default=list,
        help_text="List of aligned Sustainable Development Goals"
    )
    
    # History
    history = models.JSONField(default=list, help_text="Transaction and event history")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"NFT: {self.name} (Token: {self.token_id})"
    
    @property
    def is_funded(self):
        return self.current_funding >= self.funding_threshold
    
    @property
    def funding_percentage(self):
        if self.funding_threshold == 0:
            return 100
        return (self.current_funding / self.funding_threshold) * 100
    
    @property
    def impact_score(self):
        """Calculate overall impact score"""
        return (self.heritage_value + self.sustainability_score) / 2
    
    def append_history(self, action, details=None):
        """Append an action to the NFT history"""
        from datetime import datetime
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details or {}
        }
        self.history.append(entry)
        self.save()


class Ownership(models.Model):
    """
    Represents ownership of an NFT by a creator.
    Supports fractional and dynamic ownership.
    """
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name='ownerships')
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='nft_ownerships')
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Ownership percentage"
    )
    
    # Dynamic ownership rules
    transfer_rule = models.TextField(blank=True, help_text="Rule for ownership transfer")
    decay_rule = models.TextField(blank=True, help_text="Rule for ownership decay")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['nft', 'creator']
        ordering = ['-percentage']
        
    def __str__(self):
        return f"{self.creator} owns {self.percentage}% of {self.nft}"
    
    def clean(self):
        """Ensure total ownership doesn't exceed 100%"""
        from django.core.exceptions import ValidationError
        
        total = Ownership.objects.filter(nft=self.nft).exclude(pk=self.pk).aggregate(
            total=models.Sum('percentage')
        )['total'] or 0
        
        if total + self.percentage > 100:
            raise ValidationError(f"Total ownership would exceed 100% (current: {total}%)")


class Utility(models.Model):
    """
    Represents utilities attached to NFTs.
    """
    UTILITY_TYPES = [
        ('provenance', 'Provenance'),
        ('resale_rights', 'Resale Rights'),
        ('streaming_rights', 'Streaming Rights'),
        ('royalties', 'Royalties'),
        ('redeem_physical', 'Redeem Physical Item'),
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
    
    # Utility gating
    ownership_requirement = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Minimum ownership percentage required to access this utility"
    )
    condition = models.CharField(
        max_length=200,
        blank=True,
        help_text="Additional condition for accessing this utility"
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Utilities"
        unique_together = ['nft', 'utility_type']
        
    def __str__(self):
        return f"{self.get_utility_type_display()} for {self.nft}"
    
    def can_access(self, creator):
        """Check if a creator can access this utility"""
        try:
            ownership = self.nft.ownerships.get(creator=creator)
            return ownership.percentage >= self.ownership_requirement
        except Ownership.DoesNotExist:
            return False


class GovernanceVote(models.Model):
    """
    Represents governance voting rights for NFT holders.
    """
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name='governance_votes')
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='governance_votes')
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Vote weight (0 to 1)"
    )
    is_reputation_weighted = models.BooleanField(
        default=True,
        help_text="Whether vote weight is adjusted by creator reputation"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['nft', 'creator']
        
    def __str__(self):
        return f"{self.creator} vote on {self.nft} (weight: {self.weight})"
    
    @property
    def effective_weight(self):
        """Calculate effective vote weight including reputation if applicable"""
        if self.is_reputation_weighted:
            return float(self.weight) * (self.creator.reputation_score / 100)
        return float(self.weight)