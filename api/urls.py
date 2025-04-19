from django.urls import path, include
from rest_framework.routers import DefaultRouter

# ViewSets for Models
from .views import (
    BabyViewSet,
    BabyFacePhotoViewSet,
    BabyFootPrintViewSet,
    BabyRetinaPrintViewSet,
    MotherInfoViewSet,
    MotherIDViewSet,
    BottleQRCodeViewSet,
    EBMBottleViewSet,
    EBMUseViewSet,
)

from .views import StartMilkVerificationView, VerifyWithMotherIDView, NurseTwoVerifyView


# DRF Router
router = DefaultRouter()
router.register(r'babies', BabyViewSet)
router.register(r'baby-face-photos', BabyFacePhotoViewSet)
router.register(r'baby-foot-prints', BabyFootPrintViewSet)
router.register(r'baby-retina-prints', BabyRetinaPrintViewSet)
router.register(r'mother-info', MotherInfoViewSet)
router.register(r'mother-id', MotherIDViewSet)
router.register(r'bottle-qr-codes', BottleQRCodeViewSet)
router.register(r'ebm-bottles', EBMBottleViewSet)
router.register(r'ebm-use', EBMUseViewSet)

# URL Patterns
urlpatterns = [
    path('', include(router.urls)),
    path('milk/start-verification/', StartMilkVerificationView.as_view(), name='start-milk-verification'),
    path('milk/verify-mother-id/', VerifyWithMotherIDView.as_view(), name='verify-with-mother-id'),
    path('milk/verify-second-nurse/<int:verification_id>/', NurseTwoVerifyView.as_view(), name='nurse-two-verify'),
]
