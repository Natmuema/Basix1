"""
URL configuration for marketplace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from core.views import (
    SkillViewSet,
    CreatorViewSet,
    ProductViewSet,
    UtilityViewSet,
    NFTViewSet,
    NFTOwnershipViewSet,
    DynamicOwnershipRuleViewSet,
    GovernanceVoteViewSet,
    SDGTagViewSet,
    ImpactScoreViewSet,
    FundingThresholdViewSet,
    UtilityGateViewSet,
    NFTActionHistoryViewSet,
)

router = DefaultRouter()
router.register(r'skills', SkillViewSet)
router.register(r'creators', CreatorViewSet)
router.register(r'products', ProductViewSet)
router.register(r'utilities', UtilityViewSet)
router.register(r'nfts', NFTViewSet)
router.register(r'ownerships', NFTOwnershipViewSet)
router.register(r'dynamic-ownership-rules', DynamicOwnershipRuleViewSet)
router.register(r'governance-votes', GovernanceVoteViewSet)
router.register(r'sdg-tags', SDGTagViewSet)
router.register(r'impact-scores', ImpactScoreViewSet)
router.register(r'funding-thresholds', FundingThresholdViewSet)
router.register(r'utility-gates', UtilityGateViewSet)
router.register(r'history', NFTActionHistoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/', include(router.urls)),
]
