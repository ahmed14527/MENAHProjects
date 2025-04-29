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



class EBMUseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EBMUse
        fields = ['ebm_bottle', 'volume_used_ml']

    def create(self, validated_data):
        return EBMUse.objects.create(**validated_data)
    
    
class EBMUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EBMUse
        fields = '__all__'
        
        
            
class EBMUseStatsSerializer(serializers.Serializer):
    total_used_bottles = serializers.IntegerField()
    total_volume_used = serializers.FloatField()
    total_milk_discards = serializers.IntegerField()
    total_variable_ebm_bottles = serializers.IntegerField()


class MilkVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilkVerification
        fields = '__all__'
        read_only_fields = ['verified', 'status', 'timestamp']


