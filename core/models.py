from django.db import models
from django.utils import timezone


class Creator(models.Model):
    name = models.CharField(max_length=100, unique=True)
    wallet = models.CharField(max_length=255, unique=True)
    skills = models.JSONField(default=list, blank=True)
    reputation_score = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return f"{self.name}"

    @property
    def is_creator(self) -> bool:
        return self.ownerships.exists()


class Product(models.Model):
    TYPE_CHOICES = [
        ("ArtCraft", "Art & Crafts"),
        ("Music", "Music"),
        ("Fashion", "Fashion"),
        ("Tourism", "Tourism"),
        ("Heritage", "Heritage"),
        ("Software", "Software"),
    ]

    name = models.CharField(max_length=150, unique=True)
    type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=120, blank=True)
    physical = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    digital_scan = models.BooleanField(default=False)
    redeemable = models.BooleanField(default=False)
    license_based = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return f"{self.name} ({self.type})"


class NFT(models.Model):
    code = models.CharField(max_length=150, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="nfts")

    class Meta:
        ordering = ["code"]

    def __str__(self) -> str:  # pragma: no cover
        return self.code

    def append_history(self, action: str) -> "NFTEvent":
        return NFTEvent.objects.create(nft=self, action=action)


class NFTEvent(models.Model):
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name="events")
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at", "id"]


class UtilityType(models.TextChoices):
    PROVENANCE = "provenance", "provenance"
    RESALE_RIGHTS = "resale_rights", "resale_rights"
    STREAMING_RIGHTS = "streaming_rights", "streaming_rights"
    ROYALTIES = "royalties", "royalties"
    REDEEM_PHYSICAL = "redeem_physical", "redeem_physical"
    DIGITAL_WEARABLE = "digital_wearable", "digital_wearable"
    REDEEMABLE_EXPERIENCE = "redeemable_experience", "redeemable_experience"
    ECO_TOURISM_SUPPORT = "eco_tourism_support", "eco_tourism_support"
    ARCHIVE_ACCESS = "archive_access", "archive_access"
    PRESERVATION_FUNDING = "preservation_funding", "preservation_funding"
    LICENSE_KEY = "license_key", "license_key"
    SUBSCRIPTION_ACCESS = "subscription_access", "subscription_access"
    ROYALTY_SHARE = "royalty_share", "royalty_share"
    LIFETIME_ACCESS = "lifetime_access", "lifetime_access"
    IN_GAME_ASSETS = "in_game_assets", "in_game_assets"
    UPDATES_ACCESS = "updates_access", "updates_access"


class NFTUtility(models.Model):
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name="utilities")
    utility_type = models.CharField(max_length=64, choices=UtilityType.choices)

    class Meta:
        unique_together = ("nft", "utility_type")
        ordering = ["nft__code", "utility_type"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.nft.code}:{self.utility_type}"


class UtilityGate(models.Model):
    nft_utility = models.ForeignKey(NFTUtility, on_delete=models.CASCADE, related_name="gates")
    condition = models.CharField(max_length=255)

    class Meta:
        ordering = ["nft_utility__nft__code", "nft_utility__utility_type", "id"]


class Ownership(models.Model):
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name="ownerships")
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name="ownerships")
    percentage = models.DecimalField(max_digits=6, decimal_places=3)  # allow 0-100.000

    class Meta:
        unique_together = ("nft", "creator")
        ordering = ["nft__code", "-percentage"]


class DynamicOwnershipRule(models.Model):
    RULE_TYPE_CHOICES = [
        ("transfer_rule", "transfer_rule"),
        ("decay_rule", "decay_rule"),
    ]

    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name="dynamic_rules")
    rule_type = models.CharField(max_length=32, choices=RULE_TYPE_CHOICES)
    description = models.CharField(max_length=255)

    class Meta:
        ordering = ["nft__code", "rule_type", "id"]


class GovernanceVote(models.Model):
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name="governance_votes")
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name="governance_votes")
    weight = models.FloatField()
    reputation_weighted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("nft", "creator")
        ordering = ["nft__code", "-weight"]


class ImpactScore(models.Model):
    nft = models.OneToOneField(NFT, on_delete=models.CASCADE, related_name="impact")
    heritage_value = models.PositiveIntegerField(default=0)
    sustainability_score = models.PositiveIntegerField(default=0)
    sdg_alignment = models.JSONField(default=list, blank=True)
    computed_value = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["nft__code"]


class FundingThreshold(models.Model):
    nft = models.OneToOneField(NFT, on_delete=models.CASCADE, related_name="funding_threshold")
    amount = models.PositiveIntegerField()

    class Meta:
        ordering = ["nft__code"]
