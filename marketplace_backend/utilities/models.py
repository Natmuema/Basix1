from django.db import models
from django.utils import timezone


class Transaction(models.Model):
    """
    Represents a transaction in the marketplace.
    """
    TRANSACTION_TYPES = [
        ('mint', 'Mint'),
        ('transfer', 'Transfer'),
        ('sale', 'Sale'),
        ('funding', 'Funding Contribution'),
        ('utility_redemption', 'Utility Redemption'),
    ]
    
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    nft = models.ForeignKey('nfts.NFT', on_delete=models.CASCADE, related_name='transactions')
    from_creator = models.ForeignKey(
        'creators.Creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions_sent'
    )
    to_creator = models.ForeignKey(
        'creators.Creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions_received'
    )
    
    # Transaction details
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ownership_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Ownership percentage transferred"
    )
    
    # Blockchain data
    transaction_hash = models.CharField(max_length=100, blank=True)
    block_number = models.BigIntegerField(null=True, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.nft} at {self.timestamp}"


class ImpactMetrics(models.Model):
    """
    Track impact metrics for NFTs over time.
    """
    nft = models.ForeignKey('nfts.NFT', on_delete=models.CASCADE, related_name='impact_metrics')
    
    # Impact scores at this point in time
    heritage_value = models.IntegerField()
    sustainability_score = models.IntegerField()
    overall_impact_score = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Community metrics
    total_supporters = models.IntegerField(default=0)
    total_funding = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Activity metrics
    transactions_count = models.IntegerField(default=0)
    utilities_redeemed = models.IntegerField(default=0)
    
    recorded_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-recorded_at']
        
    def __str__(self):
        return f"Impact metrics for {self.nft} at {self.recorded_at}"


class MarketplaceStats(models.Model):
    """
    Global marketplace statistics.
    """
    date = models.DateField(unique=True)
    
    # Creator stats
    total_creators = models.IntegerField(default=0)
    verified_creators = models.IntegerField(default=0)
    average_reputation = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # NFT stats
    total_nfts = models.IntegerField(default=0)
    funded_nfts = models.IntegerField(default=0)
    total_funding_raised = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Product stats
    total_products = models.IntegerField(default=0)
    products_by_type = models.JSONField(default=dict)
    
    # Transaction stats
    daily_transactions = models.IntegerField(default=0)
    daily_volume = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Impact stats
    average_heritage_value = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    average_sustainability_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return f"Marketplace stats for {self.date}"