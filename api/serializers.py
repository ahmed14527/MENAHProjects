from rest_framework import serializers
from .models import (
    Baby, BabyFacePhoto, BabyFootPrint, BabyRetinaPrint,
    MotherInfo, MotherID, BottleQRCode, EBMBottle,
    EBMUse, MilkVerification
)

class BabySerializer(serializers.ModelSerializer):
    class Meta:
        model = Baby
        fields = '__all__'


class BabyFacePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BabyFacePhoto
        fields = '__all__'


class BabyFootPrintSerializer(serializers.ModelSerializer):
    class Meta:
        model = BabyFootPrint
        fields = '__all__'


class BabyRetinaPrintSerializer(serializers.ModelSerializer):
    class Meta:
        model = BabyRetinaPrint
        fields = '__all__'


class MotherInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotherInfo
        fields = '__all__'


class MotherIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotherID
        fields = '__all__'


class BottleQRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BottleQRCode
        fields = '__all__'


class EBMBottleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EBMBottle
        fields = '__all__'


class EBMUseSerializer(serializers.ModelSerializer):
    discarded_volume_ml = serializers.FloatField(read_only=True)

    class Meta:
        model = EBMUse
        fields = '__all__'





class MilkVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilkVerification
        fields = '__all__'
        read_only_fields = ['verified', 'status', 'timestamp']


