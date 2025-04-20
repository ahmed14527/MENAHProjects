from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserViewSet,
    RegisterView,
    CustomTokenObtainPairView,
    LoginHistoryListView,
    UserProfileView,
    AllUserProfilesView,
    UserProfileDetailView
)

# Initialize the router and register viewsets
router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

# Define URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login-history/', LoginHistoryListView.as_view(), name='login-history'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profiles/', AllUserProfilesView.as_view(), name='all-user-profiles'),
    path('profiles/<int:id>/', UserProfileDetailView.as_view(), name='user-profile-detail'),


]
