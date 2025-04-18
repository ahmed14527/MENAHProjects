from rest_framework import viewsets
from .models import (
    Baby, BabyFacePhoto, BabyFootPrint, BabyRetinaPrint,
    MotherInfo, MotherID, BottleQRCode, EBMBottle,
    EBMUse, Verification
)
from .serializers import (
    BabySerializer, BabyFacePhotoSerializer, BabyFootPrintSerializer, BabyRetinaPrintSerializer,
    MotherInfoSerializer, MotherIDSerializer, BottleQRCodeSerializer, EBMBottleSerializer,
    EBMUseSerializer, VerificationSerializer
)


class BabyViewSet(viewsets.ModelViewSet):
    queryset = Baby.objects.all()
    serializer_class = BabySerializer


class BabyFacePhotoViewSet(viewsets.ModelViewSet):
    queryset = BabyFacePhoto.objects.all()
    serializer_class = BabyFacePhotoSerializer


class BabyFootPrintViewSet(viewsets.ModelViewSet):
    queryset = BabyFootPrint.objects.all()
    serializer_class = BabyFootPrintSerializer


class BabyRetinaPrintViewSet(viewsets.ModelViewSet):
    queryset = BabyRetinaPrint.objects.all()
    serializer_class = BabyRetinaPrintSerializer


class MotherInfoViewSet(viewsets.ModelViewSet):
    queryset = MotherInfo.objects.all()
    serializer_class = MotherInfoSerializer


class MotherIDViewSet(viewsets.ModelViewSet):
    queryset = MotherID.objects.all()
    serializer_class = MotherIDSerializer


class BottleQRCodeViewSet(viewsets.ModelViewSet):
    queryset = BottleQRCode.objects.all()
    serializer_class = BottleQRCodeSerializer


class EBMBottleViewSet(viewsets.ModelViewSet):
    queryset = EBMBottle.objects.all()
    serializer_class = EBMBottleSerializer


class EBMUseViewSet(viewsets.ModelViewSet):
    queryset = EBMUse.objects.all()
    serializer_class = EBMUseSerializer


class VerificationViewSet(viewsets.ModelViewSet):
    queryset = Verification.objects.all()
    serializer_class = VerificationSerializer
