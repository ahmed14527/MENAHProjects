from rest_framework import viewsets, throttling
from rest_framework.permissions import SAFE_METHODS
from .models import (
    Baby, BabyFacePhoto, BabyFootPrint, BabyRetinaPrint,
    MotherInfo, MotherID, BottleQRCode, EBMBottle,
    EBMUse
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import MilkVerification
from .serializers import MilkVerificationSerializer

from .models import Baby
from .models import EBMBottle
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from .serializers import (
    BabySerializer, BabyFacePhotoSerializer, BabyFootPrintSerializer, BabyRetinaPrintSerializer,
    MotherInfoSerializer, MotherIDSerializer, BottleQRCodeSerializer, EBMBottleSerializer,
    EBMUseSerializer
)

from .models import EBMBottle, Baby, MotherInfo


class StandardAnonThrottle(throttling.AnonRateThrottle):
    rate = '10/minute'

class StandardUserThrottle(throttling.UserRateThrottle):
    rate = '100/hour'

class ThrottleMixin:
    throttle_classes = [StandardAnonThrottle, StandardUserThrottle]

class BabyViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = Baby.objects.all()
    serializer_class = BabySerializer

    def get_search_fields(self):
        if self.request.user.is_admin:
            return ['id', 'mother_id', 'name']
        elif self.request.user.is_nurse:
            return ['id', 'mother_id']
        return []  

class BabyFacePhotoViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = BabyFacePhoto.objects.all()
    serializer_class = BabyFacePhotoSerializer

class BabyFootPrintViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = BabyFootPrint.objects.all()
    serializer_class = BabyFootPrintSerializer

    def get_search_fields(self):
        if self.request.user.is_admin:
            return ['id', 'baby_id', 'footprint_type']
        elif self.request.user.is_nurse:
            return ['baby_id']
        return []  

class BabyRetinaPrintViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = BabyRetinaPrint.objects.all()
    serializer_class = BabyRetinaPrintSerializer

    def get_search_fields(self):
        if self.request.user.is_admin:
            return ['id', 'baby_id', 'retina_type']
        elif self.request.user.is_nurse:
            return ['baby_id']
        return []  

class MotherInfoViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = MotherInfo.objects.all()
    serializer_class = MotherInfoSerializer

    def get_search_fields(self):
        if self.request.user.is_admin:
            return ['id', 'mother_name', 'mother_id']
        elif self.request.user.is_nurse:
            return ['mother_id']
        return [] 

class MotherIDViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = MotherID.objects.all()
    serializer_class = MotherIDSerializer

    def get_search_fields(self):
        if self.request.user.is_admin:
            return ['id', 'mother_id']
        elif self.request.user.is_nurse:
            return ['mother_id']
        return []  

class BottleQRCodeViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = BottleQRCode.objects.all()
    serializer_class = BottleQRCodeSerializer

class EBMBottleViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = EBMBottle.objects.all()
    serializer_class = EBMBottleSerializer

    def get_search_fields(self):
        if self.request.user.is_admin:
            return ['id', 'ebm_bottle_id', 'baby_id']
        elif self.request.user.is_nurse:
            return ['baby_id']
        return []  

class EBMUseViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = EBMUse.objects.all()
    serializer_class = EBMUseSerializer


class StartMilkVerificationView(ThrottleMixin,APIView):

    def post(self, request):
        data = request.data
        baby_id = data.get('baby_id')
        bottle_id = data.get('bottle_id')

        baby = get_object_or_404(Baby, id=baby_id)
        bottle = get_object_or_404(EBMBottle, id=bottle_id)

        verification = MilkVerification.objects.create(
            baby=baby,
            bottle=bottle,
            nurse_one=request.user
        )

        return Response({
            "message": "Step 1 complete. Awaiting Nurse 2 verification.",
            "verification_id": verification.id
        })


class VerifyWithMotherIDView(ThrottleMixin,APIView):

    def post(self, request):
        data = request.data
        bottle_id = data.get('bottle_id')
        baby_id = data.get('baby_id')
        match_with_mother = data.get('match_with_mother')

        bottle = get_object_or_404(EBMBottle, id=bottle_id)
        baby = get_object_or_404(Baby, id=baby_id)
        verification = MilkVerification.objects.filter(bottle=bottle, baby=baby).last()

        if not verification:
            return Response({"message": "No previous verification found."}, status=400)

        if match_with_mother:
            verification.match_with_mother = True
            verification.status = 'pending'
            verification.reprint_required = True
            verification.save()
            return Response({
                "message": "Matched with mother. Please reprint bottle QR and retry verification.",
                "reprint_required": True
            })
        else:
            verification.status = 'failed'
            verification.save()
            return Response({
                "message": "❌ This milk does not belong to this baby. Do not give the milk.",
                "reprint_required": False
            }, status=403)


class NurseTwoVerifyView(ThrottleMixin,APIView):

    def post(self, request, verification_id):
        verification = get_object_or_404(MilkVerification, id=verification_id)

        if verification.nurse_two:
            return Response({"message": "Verification already completed by second nurse."}, status=400)

        if verification.status != 'pending':
            return Response({"message": "This verification is not in pending state."}, status=400)

        verification.nurse_two = request.user
        verification.verified = True
        verification.status = 'verified'
        verification.save()

        return Response({
            "message": "✅ Milk verified successfully. It is safe to feed the baby.",
            "verified": True
        })
