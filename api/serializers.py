from rest_framework import serializers
from .models import (
    Baby,
    FacePhoto,
    FootPrint,
    RetinaPrint,
    MotherID,
    Mother,
    Nurse,
    Parent,
    QRCode
)

# Baby Serializer
class BabySerializer(serializers.ModelSerializer):
    class Meta:
        model = Baby
        fields = '__all__'

# FacePhoto Serializer
class FacePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacePhoto
        fields = '__all__'

# FootPrint Serializer
class FootPrintSerializer(serializers.ModelSerializer):
    class Meta:
        model = FootPrint
        fields = '__all__'

# RetinaPrint Serializer
class RetinaPrintSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetinaPrint
        fields = '__all__'

# MotherID Serializer
class MotherIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotherID
        fields = '__all__'

# Mother Serializer
class MotherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mother
        fields = '__all__'

# Nurse Serializer
class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = '__all__'

# Parent Serializer
class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'


class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = '__all__'