from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    MeView,
    UsageInfoView,
    APIKeyViewSet,
)

router = SimpleRouter()
router.register(r'keys', APIKeyViewSet, basename='api-key')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/me/', MeView.as_view(), name='me'),
    path('usage/', UsageInfoView.as_view(), name='usage'),
    path('', include(router.urls)),
]
