from decimal import Decimal
from django.db.models import Sum, Avg, Count, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from django.db import models


def calculate_impact_score(nft):
    """
    Calculate the overall impact score for an NFT.
    Considers heritage value, sustainability, and creator reputation.
    """
    # Base impact from heritage and sustainability
    base_impact = (nft.heritage_value + nft.sustainability_score) / 2
    
    # Get average creator reputation
    creator_reputations = [
        ownership.creator.reputation_score 
        for ownership in nft.ownerships.all()
    ]
    avg_reputation = sum(creator_reputations) / len(creator_reputations) if creator_reputations else 50
    
    # Weight the impact score with creator reputation
    weighted_impact = (base_impact * 0.7) + (avg_reputation * 0.3)
    
    return round(weighted_impact, 2)


def check_funding_threshold(nft):
    """
    Check if an NFT has reached its funding threshold.
    """
    return nft.current_funding >= nft.funding_threshold


def calculate_ownership_distribution(nft):
    """
    Calculate the ownership distribution for an NFT.
    Returns a dictionary with creator names and percentages.
    """
    distribution = {}
    for ownership in nft.ownerships.all():
        creator_name = ownership.creator.user.username if ownership.creator.user else f"Creator {ownership.creator.id}"
        distribution[creator_name] = {
            'percentage': float(ownership.percentage),
            'wallet': ownership.creator.wallet_address,
            'reputation': ownership.creator.reputation_score
        }
    return distribution


def apply_dynamic_ownership_rules(ownership):
    """
    Apply dynamic ownership rules based on conditions.
    This would be called periodically or triggered by events.
    """
    # Example: Apply transfer rule
    if ownership.transfer_rule:
        # Parse and apply the rule (simplified example)
        if "contributes 100 sales" in ownership.transfer_rule:
            # Check sales contribution logic here
            pass
    
    # Example: Apply decay rule
    if ownership.decay_rule:
        # Parse and apply the rule (simplified example)
        if "reduces by 5% if not maintained" in ownership.decay_rule:
            # Check maintenance logic here
            pass


def calculate_effective_governance_weight(nft):
    """
    Calculate the total effective governance weight for an NFT.
    Takes into account reputation weighting.
    """
    total_weight = Decimal('0')
    for vote in nft.governance_votes.all():
        total_weight += Decimal(str(vote.effective_weight))
    return float(total_weight)


def get_accessible_utilities(nft, creator):
    """
    Get all utilities accessible to a creator for a given NFT.
    """
    accessible_utilities = []
    
    try:
        ownership = nft.ownerships.get(creator=creator)
        ownership_percentage = ownership.percentage
    except:
        ownership_percentage = 0
    
    for utility in nft.utilities.filter(is_active=True):
        if ownership_percentage >= utility.ownership_requirement:
            # Check additional conditions if any
            if not utility.condition or evaluate_condition(utility.condition, creator, nft):
                accessible_utilities.append(utility)
    
    return accessible_utilities


def evaluate_condition(condition, creator, nft):
    """
    Evaluate custom conditions for utility access.
    This is a simplified implementation.
    """
    if "subscription_active" in condition:
        # Check subscription status (placeholder logic)
        return True
    
    # Add more condition evaluations as needed
    return True


def update_creator_reputation(creator, action_type, value=1):
    """
    Update creator reputation based on actions.
    """
    reputation_changes = {
        'nft_minted': 5,
        'sale_completed': 3,
        'utility_redeemed': 2,
        'positive_feedback': 1,
        'negative_feedback': -2,
        'dispute_resolved': -5,
    }
    
    change = reputation_changes.get(action_type, value)
    creator.reputation_score = max(0, min(100, creator.reputation_score + change))
    creator.save()
    
    return creator.reputation_score


def generate_marketplace_stats(date=None):
    """
    Generate marketplace statistics for a given date.
    """
    from creators.models import Creator
    from products.models import Product
    from nfts.models import NFT
    from .models import MarketplaceStats, Transaction
    
    if not date:
        date = timezone.now().date()
    
    # Calculate creator stats
    total_creators = Creator.objects.count()
    verified_creators = Creator.objects.filter(
        nfts_created__isnull=False
    ).distinct().count()
    average_reputation = Creator.objects.aggregate(
        avg_rep=Avg('reputation_score')
    )['avg_rep'] or 0
    
    # Calculate NFT stats
    total_nfts = NFT.objects.count()
    funded_nfts = NFT.objects.filter(
        current_funding__gte=models.F('funding_threshold')
    ).count()
    total_funding_raised = NFT.objects.aggregate(
        total=Sum('current_funding')
    )['total'] or 0
    
    # Calculate product stats
    total_products = Product.objects.count()
    products_by_type = Product.objects.values('product_type').annotate(
        count=Count('id')
    )
    products_dict = {item['product_type']: item['count'] for item in products_by_type}
    
    # Calculate transaction stats for the day
    start_time = datetime.combine(date, datetime.min.time())
    end_time = datetime.combine(date, datetime.max.time())
    
    daily_transactions = Transaction.objects.filter(
        timestamp__range=(start_time, end_time)
    ).count()
    
    daily_volume = Transaction.objects.filter(
        timestamp__range=(start_time, end_time),
        amount__isnull=False
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Calculate impact stats
    average_heritage = NFT.objects.aggregate(
        avg=Avg('heritage_value')
    )['avg'] or 0
    
    average_sustainability = NFT.objects.aggregate(
        avg=Avg('sustainability_score')
    )['avg'] or 0
    
    # Create or update stats
    stats, created = MarketplaceStats.objects.update_or_create(
        date=date,
        defaults={
            'total_creators': total_creators,
            'verified_creators': verified_creators,
            'average_reputation': average_reputation,
            'total_nfts': total_nfts,
            'funded_nfts': funded_nfts,
            'total_funding_raised': total_funding_raised,
            'total_products': total_products,
            'products_by_type': products_dict,
            'daily_transactions': daily_transactions,
            'daily_volume': daily_volume,
            'average_heritage_value': average_heritage,
            'average_sustainability_score': average_sustainability,
        }
    )
    
    return stats


def record_impact_metrics(nft):
    """
    Record current impact metrics for an NFT.
    """
    from .models import ImpactMetrics
    
    impact_score = calculate_impact_score(nft)
    total_supporters = nft.ownerships.count()
    transactions_count = nft.transactions.count()
    utilities_redeemed = nft.transactions.filter(
        transaction_type='utility_redemption'
    ).count()
    
    metrics = ImpactMetrics.objects.create(
        nft=nft,
        heritage_value=nft.heritage_value,
        sustainability_score=nft.sustainability_score,
        overall_impact_score=impact_score,
        total_supporters=total_supporters,
        total_funding=nft.current_funding,
        transactions_count=transactions_count,
        utilities_redeemed=utilities_redeemed,
    )
    
    return metrics