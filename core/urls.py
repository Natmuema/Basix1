from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CreatorViewSet,
    ProductViewSet,
    NFTViewSet,
    NFTEventViewSet,
    NFTUtilityViewSet,
    UtilityGateViewSet,
    OwnershipViewSet,
    DynamicOwnershipRuleViewSet,
    GovernanceVoteViewSet,
    ImpactScoreViewSet,
    FundingThresholdViewSet,
)


router = DefaultRouter()
router.register(r"creators", CreatorViewSet)
router.register(r"products", ProductViewSet)
router.register(r"nfts", NFTViewSet)
router.register(r"events", NFTEventViewSet)
router.register(r"utilities", NFTUtilityViewSet)
router.register(r"utility-gates", UtilityGateViewSet)
router.register(r"ownerships", OwnershipViewSet)
router.register(r"dynamic-ownership-rules", DynamicOwnershipRuleViewSet)
router.register(r"governance-votes", GovernanceVoteViewSet)
router.register(r"impact-scores", ImpactScoreViewSet)
router.register(r"funding-thresholds", FundingThresholdViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

