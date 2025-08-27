from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'auth', views.AuthViewSet, basename='auth')
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
router.register(r'smart-functions', views.SmartFunctionViewSet)
router.register(r'marketplace-configs', views.MarketplaceConfigViewSet)
router.register(r'stats', views.MarketplaceStatsViewSet, basename='stats')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('api/', include(router.urls)),
]