from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserView,
    CustomTokenObtainPairView,
    RegistrationView
)

router = DefaultRouter()
router.register(r'', UserView, basename='user')
router.register(r'reg', RegistrationView, basename='registration')  # Corrected 'Registrastion' to 'registration'

urlpatterns = [
    # Authentication endpoints
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Router URLs
    path('', include(router.urls)),
] 