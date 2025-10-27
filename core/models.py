from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Creator(TimestampedModel):
    name = models.CharField(max_length=120, unique=True)
    wallet_address = models.CharField(max_length=200, unique=True)
    reputation_score = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    skills = models.ManyToManyField(Skill, related_name="creators", blank=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.wallet_address})"

    @property
    def is_creator(self) -> bool:
        # A user is a creator if they have minted/own at least one NFT (ownership entry exists)
        return self.ownerships.exists()


class Product(TimestampedModel):
    name = models.CharField(max_length=150, unique=True)
    type = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=120, blank=True)

    physical = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    digital_scan = models.BooleanField(default=False)
    redeemable = models.BooleanField(default=False)
    license_based = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name} [{self.type}]"


class Utility(models.Model):
    code = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.code


class NFT(TimestampedModel):
    code = models.CharField(max_length=150, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="nfts")
    utilities = models.ManyToManyField(Utility, related_name="nfts", blank=True)

    def __str__(self) -> str:
        return self.code


class NFTOwnership(TimestampedModel):
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name="ownerships")
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name="ownerships")
    percentage = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        unique_together = ("nft", "creator")

    def __str__(self) -> str:
        return f"{self.nft.code}: {self.creator.name} {self.percentage}%"


class DynamicOwnershipRule(TimestampedModel):
    RULE_TYPE_CHOICES = (
        ("transfer_rule", "Transfer Rule"),
        ("decay_rule", "Decay Rule"),
    )

    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name="dynamic_rules")
    creator = models.ForeignKey(Creator, on_delete=models.SET_NULL, null=True, blank=True)
    rule_type = models.CharField(max_length=32, choices=RULE_TYPE_CHOICES)
    rule_text = models.TextField()

    def __str__(self) -> str:
        who = self.creator.name if self.creator else "global"
        return f"{self.nft.code} {self.rule_type} for {who}"


class GovernanceVote(TimestampedModel):
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name="governance_votes")
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name="governance_votes")
    weight = models.DecimalField(max_digits=6, decimal_places=3, validators=[MinValueValidator(0)])
    reputation_weighted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("nft", "creator")

    def __str__(self) -> str:
        return f"Vote {self.weight} by {self.creator.name} on {self.nft.code}"


class SDGTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class ImpactScore(TimestampedModel):
    nft = models.OneToOneField(NFT, on_delete=models.CASCADE, related_name="impact")
    heritage_value = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    sustainability_score = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    sdg_alignment = models.ManyToManyField(SDGTag, related_name="impacts", blank=True)

    def __str__(self) -> str:
        return f"Impact for {self.nft.code}"


class FundingThreshold(TimestampedModel):
    nft = models.OneToOneField(NFT, on_delete=models.CASCADE, related_name="funding_threshold")
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self) -> str:
        return f"Funding {self.amount} for {self.nft.code}"


class UtilityGate(TimestampedModel):
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name="utility_gates")
    utility = models.ForeignKey(Utility, on_delete=models.CASCADE, related_name="gates")
    condition = models.CharField(max_length=200)

    class Meta:
        unique_together = ("nft", "utility", "condition")

    def __str__(self) -> str:
        return f"Gate {self.utility.code} on {self.nft.code}: {self.condition}"


class NFTActionHistory(TimestampedModel):
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name="history")
    action = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.nft.code}: {self.action} @ {self.created_at}"

