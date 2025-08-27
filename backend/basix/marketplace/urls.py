from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'creators', views.CreatorViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'nfts', views.NFTViewSet)
router.register(r'utilities', views.UtilityViewSet)
router.register(r'ownerships', views.OwnershipViewSet)
router.register(r'dynamic-ownerships', views.DynamicOwnershipViewSet)
router.register(r'governance-votes', views.GovernanceVoteViewSet)
router.register(r'utility-gates', views.UtilityGateViewSet)
router.register(r'impact-scores', views.ImpactScoreViewSet)
router.register(r'funding-thresholds', views.FundingThresholdViewSet)
router.register(r'nft-history', views.NFTHistoryViewSet)
router.register(r'marketplace-stats', views.MarketplaceStatsViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]