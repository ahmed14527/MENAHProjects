from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('nurse', 'Nurse'),
    ('parent', 'Parent'),
)

class User(AbstractUser):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class MilkRecord(models.Model):
    baby_name = models.CharField(max_length=100)
    milk_amount_ml = models.FloatField()
    date_given = models.DateTimeField(auto_now_add=True)
    nurse = models.ForeignKey(User, on_delete=models.CASCADE, related_name='milk_records')

    def __str__(self):
        return f"{self.baby_name} - {self.date_given.strftime('%Y-%m-%d')}"

class QRCode(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    milk_record = models.OneToOneField(MilkRecord, on_delete=models.CASCADE, related_name='qr_code')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_qrcodes')
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"QR-{self.code} for {self.milk_record.baby_name}"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
