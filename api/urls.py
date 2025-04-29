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
    BabyEBMUseStatsAPIView,
    StartMilkVerificationView,
    VerifyWithMotherIDView,
    NurseTwoVerifyView,
    VerifyFootprintWithQRCodeView,
    VerifyFaceWithQRCodeView,
    VerifyRetinaWithQRCodeView,
    VerifyMotherFingerprintOrIDView,
    EBMUseViewSet
)



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
router.register(r'ebm-uses', EBMUseViewSet, basename='ebm-use')


# URL Patterns
urlpatterns = [
    path('', include(router.urls)),
    path('babies/<int:baby_id>/ebm-use-stats/', BabyEBMUseStatsAPIView.as_view(), name='baby-ebm-use-stats'),
    path('start-verification/', StartMilkVerificationView.as_view(), name='start_milk_verification'),
    path('verify-with-mother-id/', VerifyWithMotherIDView.as_view(), name='verify_with_mother_id'),
    path('nurse-two-verify/<int:verification_id>/', NurseTwoVerifyView.as_view(), name='nurse_two_verify'),

    path('verify-footprint-qr/', VerifyFootprintWithQRCodeView.as_view(), name='verify_footprint_qr'),
    path('verify-face-qr/', VerifyFaceWithQRCodeView.as_view(), name='verify_face_qr'),
    path('verify-retina-qr/', VerifyRetinaWithQRCodeView.as_view(), name='verify_retina_qr'),
    path('verify-mother-id-fingerprint/', VerifyMotherFingerprintOrIDView.as_view(), name='verify_mother_id_fingerprint'),
]
