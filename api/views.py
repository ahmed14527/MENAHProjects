# Imports
from rest_framework import viewsets, throttling, status
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import (
    Baby, BabyFacePhoto, BabyFootPrint, BabyRetinaPrint,
    MotherInfo, MotherID, BottleQRCode, EBMBottle,
    EBMUse, MilkVerification
)
from .serializers import (
    BabySerializer, BabyFacePhotoSerializer, BabyFootPrintSerializer, BabyRetinaPrintSerializer,
    MotherInfoSerializer, MotherIDSerializer, BottleQRCodeSerializer, EBMBottleSerializer,
    MilkVerificationSerializer,EBMUseSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Sum

from .models import Baby, EBMBottle, EBMUse
from .serializers import EBMUseStatsSerializer

# Throttling
class StandardAnonThrottle(throttling.AnonRateThrottle):
    rate = '10/minute'

class StandardUserThrottle(throttling.UserRateThrottle):
    rate = '100/hour'

class ThrottleMixin:
    throttle_classes = [StandardAnonThrottle, StandardUserThrottle]


# ViewSets
class BabyViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = Baby.objects.all()
    serializer_class = BabySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]

    def get_search_fields(self):
        return ['id', 'mrn', 'name_en', 'name_ar']

class BabyFacePhotoViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = BabyFacePhoto.objects.all()
    serializer_class = BabyFacePhotoSerializer

class BabyFootPrintViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = BabyFootPrint.objects.all()
    serializer_class = BabyFootPrintSerializer

    

class BabyRetinaPrintViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = BabyRetinaPrint.objects.all()
    serializer_class = BabyRetinaPrintSerializer

    

class MotherInfoViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = MotherInfo.objects.all()
    serializer_class = MotherInfoSerializer

    

class MotherIDViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = MotherID.objects.all()
    serializer_class = MotherIDSerializer

    

class BottleQRCodeViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = BottleQRCode.objects.all()
    serializer_class = BottleQRCodeSerializer

class EBMBottleViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = EBMBottle.objects.all()
    serializer_class = EBMBottleSerializer

    
class EBMUseViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = EBMUse.objects.all()
    serializer_class = EBMUseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]

    def get_search_fields(self):
        return ['id', 'ebm_bottle__id', 'volume_used_ml']
    
    
    

class BabyEBMUseStatsAPIView(APIView):

    def get(self, request, baby_id, *args, **kwargs):
        baby = get_object_or_404(Baby, id=baby_id)

        bottles = EBMBottle.objects.filter(baby=baby)

        uses = EBMUse.objects.filter(ebm_bottle__in=bottles)

        total_used_bottles = uses.count()
        total_volume_used = uses.aggregate(total=Sum('volume_used_ml'))['total'] or 0
        total_milk_discards = uses.filter(discarded_volume_ml__gt=0).count()
        total_variable_ebm_bottles = bottles.filter(variable_volume=True).count()

        stats = {
            "total_used_bottles": total_used_bottles,
            "total_volume_used": total_volume_used,
            "total_milk_discards": total_milk_discards,
            "total_variable_ebm_bottles": total_variable_ebm_bottles,
        }

        serializer = EBMUseStatsSerializer(stats)
        return Response(serializer.data)



# Milk Verification Views
class StartMilkVerificationView(ThrottleMixin, APIView):

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


class VerifyWithMotherIDView(ThrottleMixin, APIView):

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


class NurseTwoVerifyView(ThrottleMixin, APIView):

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


# New Verifications (Footprint, Face, Retina, Mother ID)
class VerifyFootprintWithQRCodeView(ThrottleMixin, APIView):

    def post(self, request):
        baby_id = request.data.get('baby_id')
        qr_unique_number = request.data.get('qr_unique_number')

        baby = get_object_or_404(Baby, id=baby_id)
        footprint = BabyFootPrint.objects.filter(baby=baby).last()
        bottle_qr = EBMBottle.objects.filter(unique_number=qr_unique_number, baby=baby).last()

        if footprint and bottle_qr:
            return Response({"message": "✅ Baby footprint and QR code match found.", "matched": True})
        else:
            return Response({"message": "❌ Footprint or QR code does not match.", "matched": False}, status=400)


class VerifyFaceWithQRCodeView(ThrottleMixin, APIView):

    def post(self, request):
        baby_id = request.data.get('baby_id')
        qr_unique_number = request.data.get('qr_unique_number')

        baby = get_object_or_404(Baby, id=baby_id)
        face_photo = BabyFacePhoto.objects.filter(baby=baby).last()
        bottle_qr = EBMBottle.objects.filter(unique_number=qr_unique_number, baby=baby).last()

        if face_photo and bottle_qr:
            return Response({"message": "✅ Baby face photo and QR code match found.", "matched": True})
        else:
            return Response({"message": "❌ Face photo or QR code does not match.", "matched": False}, status=400)


class VerifyRetinaWithQRCodeView(ThrottleMixin, APIView):

    def post(self, request):
        baby_id = request.data.get('baby_id')
        qr_unique_number = request.data.get('qr_unique_number')

        baby = get_object_or_404(Baby, id=baby_id)
        retina_print = BabyRetinaPrint.objects.filter(baby=baby).last()
        bottle_qr = EBMBottle.objects.filter(unique_number=qr_unique_number, baby=baby).last()

        if retina_print and bottle_qr:
            return Response({"message": "✅ Baby retina print and QR code match found.", "matched": True})
        else:
            return Response({"message": "❌ Retina print or QR code does not match.", "matched": False}, status=400)


class VerifyMotherFingerprintOrIDView(ThrottleMixin, APIView):

    def post(self, request):
        baby_id = request.data.get('baby_id')
        mother_id_provided = request.data.get('mother_id_provided', False)
        mother_fingerprint_provided = request.data.get('mother_fingerprint_provided', False)

        baby = get_object_or_404(Baby, id=baby_id)
        mother_id = MotherID.objects.filter(baby=baby).last()

        if mother_id_provided or mother_fingerprint_provided:
            if mother_id:
                return Response({"message": "✅ Mother identity or fingerprint verified.", "matched": True})
            else:
                return Response({"message": "❌ No mother ID found for verification.", "matched": False}, status=400)
        else:
            return Response({"message": "❌ No verification data provided.", "matched": False}, status=400)
