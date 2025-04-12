"""
URL configuration for chemoventry project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import CustomTokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
# Import our new report views
from inventory.reports import inventory_report, usage_report, expiry_report, low_stock_report

# Main URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth endpoints
    path('api/users/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Main API URLs
    path('api/users/', include('users.urls')),
    path('api/', include('inventory.urls')),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(permission_classes=[AllowAny]), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema', permission_classes=[AllowAny]), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema', permission_classes=[AllowAny]), name='redoc'),
    
    # NEW REPORT ENDPOINTS
    path('api/reports/inventory/', inventory_report, name='inventory_report'),
    path('api/reports/usage/', usage_report, name='usage_report'),
    path('api/reports/expiry/', expiry_report, name='expiry_report'),
    path('api/reports/low-stock/', low_stock_report, name='low_stock_report'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
