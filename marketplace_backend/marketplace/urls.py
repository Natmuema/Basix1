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
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request):
    """
    API root endpoint showing available endpoints
    """
    return Response({
        'message': 'Welcome to Marketplace API',
        'endpoints': {
            'creators': '/api/creators/',
            'products': '/api/products/',
            'nfts': '/api/nfts/',
            'transactions': '/api/transactions/',
            'impact-metrics': '/api/impact-metrics/',
            'marketplace-stats': '/api/marketplace-stats/',
            'admin': '/admin/',
        },
        'version': '1.0.0'
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/', include('creators.urls')),
    path('api/', include('products.urls')),
    path('api/', include('nfts.urls')),
    path('api/', include('utilities.urls')),
]

# Add media files serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)