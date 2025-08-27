from django.db import models


class Product(models.Model):
    """
    Represents a product in the marketplace.
    Can be physical, digital, or redeemable experiences.
    """
    PRODUCT_TYPES = [
        ('ArtCraft', 'Art & Craft'),
        ('Music', 'Music'),
        ('Fashion', 'Fashion'),
        ('Tourism', 'Tourism'),
        ('Heritage', 'Heritage'),
        ('Software', 'Software'),
    ]
    
    CATEGORIES = [
        # Art & Craft
        ('Beadwork', 'Beadwork'),
        ('Painting', 'Painting'),
        ('Sculpture', 'Sculpture'),
        # Music
        ('Afrobeat', 'Afrobeat'),
        ('Traditional', 'Traditional'),
        ('Contemporary', 'Contemporary'),
        # Fashion
        ('Textile', 'Textile'),
        ('Jewelry', 'Jewelry'),
        ('Accessories', 'Accessories'),
        # Software
        ('AI/ML', 'AI/ML'),
        ('Gaming', 'Gaming'),
        ('Tools', 'Tools'),
        # Other
        ('Other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPES)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORIES)
    
    # Product properties
    is_physical = models.BooleanField(default=False)
    is_digital = models.BooleanField(default=True)
    has_digital_scan = models.BooleanField(default=False)
    is_redeemable = models.BooleanField(default=False)
    is_license_based = models.BooleanField(default=False)
    
    # Media
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    digital_file = models.FileField(upload_to='products/files/', null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} ({self.product_type})"