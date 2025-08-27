from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'auth', views.AuthViewSet, basename='auth')
router.register(r'users', views.UserViewSet)
router.register(r'creator-profiles', views.CreatorProfileViewSet)
router.register(r'investor-profiles', views.InvestorProfileViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('api/', include(router.urls)),
]