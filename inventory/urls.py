from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LocationViewSet,
    ChemicalViewSet,
    #get_dashboard_stats,
    get_dashboard_overview,
    generate_report
)

router = DefaultRouter()
router.register(r'location', LocationViewSet, basename='Location')
router.register(r'chemical', ChemicalViewSet, basename='Chemical')

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),
    
    #path('dashboard/stats/', get_dashboard_stats, name='dashboard-stats'),
    path('dashboard/overview/', get_dashboard_overview, name='dashboard-overview'),
    
    # Reports - old endpoint (keeping for backward compatibility)
    path('reports/generate/', generate_report, name='generate_report'),
]