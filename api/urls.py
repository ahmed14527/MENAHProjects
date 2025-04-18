from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BabyViewSet, BabyFacePhotoViewSet, BabyFootPrintViewSet, BabyRetinaPrintViewSet,
    MotherInfoViewSet, MotherIDViewSet, BottleQRCodeViewSet,
    EBMBottleViewSet, EBMUseViewSet, VerificationViewSet
)

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
router.register(r'verifications', VerificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
