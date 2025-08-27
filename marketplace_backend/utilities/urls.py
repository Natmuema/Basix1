from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TransactionViewSet, ImpactMetricsViewSet, MarketplaceStatsViewSet,
    calculate_nft_impact_score, check_utility_access
)

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'impact-metrics', ImpactMetricsViewSet, basename='impact-metric')
router.register(r'marketplace-stats', MarketplaceStatsViewSet, basename='marketplace-stat')

urlpatterns = [
    path('', include(router.urls)),
    path('impact-score/', calculate_nft_impact_score, name='calculate-impact-score'),
    path('utility-access/', check_utility_access, name='check-utility-access'),
]