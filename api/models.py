from django.db import models
from django.utils.translation import gettext_lazy as _
import os
from django.conf import settings
from django.core.exceptions import ValidationError
# Upload path functions
def face_photo_upload(instance, filename):
    ext = filename.split('.')[-1]
    return f'face_photos/{instance.baby.name}_{instance.baby.mrn}.{ext}'

def footprint_upload(instance, filename):
    ext = filename.split('.')[-1]
    return f'foot_prints/{instance.baby.name}_{instance.baby.mrn}.{ext}'

def retina_upload(instance, filename):
    ext = filename.split('.')[-1]
    return f'retina_prints/{instance.baby.name}_{instance.baby.mrn}.{ext}'

def mother_id_upload(instance, filename):
    ext = filename.split('.')[-1]
    return f'mother_ids/{instance.baby.name}_{instance.baby.mrn}.{ext}'

def qr_code_upload(instance, filename):
    ext = filename.split('.')[-1]
    return f'qr_codes/{instance.baby.name}_{instance.baby.mrn}.{ext}'


# General Base Model for Baby
class Baby(models.Model):
    name = models.CharField(max_length=100)
    mrn = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField()

    def __str__(self):
        return f'{self.name} ({self.mrn})'


# Baby Face Photo
class BabyFacePhoto(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=face_photo_upload)
    captured_at = models.DateTimeField(auto_now_add=True)

# Baby Footprint
class BabyFootPrint(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=footprint_upload)
    captured_at = models.DateTimeField(auto_now_add=True)

# Baby Retina Print
class BabyRetinaPrint(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=retina_upload)
    captured_at = models.DateTimeField(auto_now_add=True)

# Mother Information
class MotherInfo(models.Model):
    baby = models.OneToOneField(Baby, on_delete=models.CASCADE)
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    mother_mrn = models.CharField(max_length=50)
    gravida = models.PositiveSmallIntegerField()
    para = models.PositiveSmallIntegerField()
    abortion = models.PositiveSmallIntegerField()
    delivery_date = models.DateField()

    class DeliveryType(models.TextChoices):
        NORMAL = 'Normal', _('Normal Vaginal Delivery')
        C_SECTION = 'C-Section', _('C-Section')

    delivery_type = models.CharField(
        max_length=10,
        choices=DeliveryType.choices,
        default=DeliveryType.NORMAL
    )

# Mother ID Scan
class MotherID(models.Model):
    baby = models.OneToOneField(Baby, on_delete=models.CASCADE)
    id_image = models.ImageField(upload_to=mother_id_upload)
    scanned_at = models.DateTimeField(auto_now_add=True)

# QR Code for bottle
class BottleQRCode(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    bottle_number = models.PositiveIntegerField()
    unique_number = models.CharField(max_length=100, unique=True)
    qr_code_image = models.ImageField(upload_to=qr_code_upload)
    created_at = models.DateTimeField(auto_now_add=True)

# EBM Delivery Record
class EBMBottle(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    date_expressed = models.DateField()
    date_delivered = models.DateField()
    bottle_number = models.PositiveIntegerField()
    unique_number = models.CharField(max_length=100, unique=True)
    volume_ml = models.FloatField()

    def __str__(self):
        return f'Bottle_{self.bottle_number}_{self.unique_number}_{self.baby.name}_{self.baby.mrn}'


# EBM Use Record
class EBMUse(models.Model):
    ebm_bottle = models.ForeignKey(EBMBottle, on_delete=models.CASCADE)
    volume_used_ml = models.FloatField()
    discarded_volume_ml = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.ebm_bottle:
            self.discarded_volume_ml = self.ebm_bottle.volume_ml - self.volume_used_ml
        super().save(*args, **kwargs)


# Verification Process


from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


def validate_nurse(user):
    if user.role != 'Nurse':
        raise ValidationError("User must be a nurse.")


class MilkVerification(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    bottle = models.ForeignKey(EBMBottle, on_delete=models.CASCADE)
    nurse_one = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='verifications_as_nurse_one',
        validators=[validate_nurse]
    )
    nurse_two = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verifications_as_nurse_two',
        validators=[validate_nurse]
    )
    verified = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('verified', 'Verified'), ('failed', 'Failed')],
        default='pending'
    )
    verify_face_with_qr = models.BooleanField(default=False)
    verify_footprint_with_qr = models.BooleanField(default=False)
    verify_retina_with_qr = models.BooleanField(default=False)
    verify_mother_id_or_fingerprint = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verification for {self.baby.name} - {self.bottle.unique_number}"