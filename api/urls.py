from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MilkRecordViewSet, QRCodeViewSet, MessageViewSet, LoginHistoryViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, CustomTokenObtainPairView

router = DefaultRouter()
router.register('milk-records', MilkRecordViewSet)
router.register('qrcodes', QRCodeViewSet)
router.register('messages', MessageViewSet)
router.register('login-history', LoginHistoryViewSet, basename='login-history')  # إضافة basename هنا

urlpatterns = [
    path('api/', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
