from django.db import models

class Baby(models.Model):
    baby_name = models.CharField(max_length=255, blank=True, null=True)
    baby_name_arabic = models.CharField(max_length=255, blank=True, null=True)
    baby_mrn = models.CharField(max_length=100, blank=True, null=True)
    visit_number = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    birth_weight = models.FloatField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    ga_weeks = models.IntegerField(blank=True, null=True)
    ga_days = models.IntegerField(blank=True, null=True)
    passport_id = models.CharField(max_length=100, blank=True, null=True)
    personal_id = models.CharField(max_length=100, blank=True, null=True)
    birth_certificate_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.baby_name or f"Baby #{self.id}"


class FacePhoto(models.Model):
    baby = models.ForeignKey(
        'Baby', 
        on_delete=models.CASCADE, 
        related_name='face_photos'
    )
    photo_path = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FacePhoto for {self.baby} uploaded at {self.uploaded_at}"
    
    
class FootPrint(models.Model):
    baby = models.ForeignKey(
        'Baby',
        on_delete=models.CASCADE,
        related_name='foot_prints'
    )
    image_path = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FootPrint for {self.baby} uploaded at {self.uploaded_at}"
    
    
class Mother(models.Model):
    mother_name = models.CharField(max_length=255)
    mother_id = models.CharField(max_length=100, unique=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mother_name
    
    
class MotherFingerPrint(models.Model):
    mother = models.ForeignKey(
        'Mother',
        on_delete=models.CASCADE,
        related_name='fingerprints'
    )
    image_path = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fingerprint for {self.mother} uploaded at {self.uploaded_at}"
    
class MotherID(models.Model):
    ID_TYPE_CHOICES = [
        ("National ID", "National ID"),
        ("Passport", "Passport"),
        ("Resident ID", "Resident ID"),
    ]

    mother = models.ForeignKey(
        'Mother',
        on_delete=models.CASCADE,
        related_name='ids'
    )
    id_type = models.CharField(max_length=20, choices=ID_TYPE_CHOICES)
    id_number = models.CharField(max_length=100)
    id_image_path = models.CharField(max_length=500, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_type} - {self.id_number} for {self.mother}"
    
    
    
class Nurse(models.Model):
    full_name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100, unique=True)
    hospital = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # يفضل استخدام نظام التوثيق المدمج في Django
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
    
class Parent(models.Model):
    RELATION_CHOICES = [
        ("Mother", "Mother"),
        ("Father", "Father"),
        ("Guardian", "Guardian"),
    ]

    full_name = models.CharField(max_length=255)
    relation_to_baby = models.CharField(max_length=20, choices=RELATION_CHOICES)
    national_id = models.CharField(max_length=100, unique=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # يُفضل تشفيرها أو استخدام نظام تسجيل دخول جاهز
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
    
class QRCode(models.Model):
    baby = models.ForeignKey(
        'Baby',
        on_delete=models.CASCADE,
        related_name='qr_codes'
    )
    qr_code_data = models.TextField()
    qr_code_image_path = models.CharField(max_length=500)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QR Code for {self.baby} generated at {self.generated_at}"
    
    
class RetinaPrint(models.Model):
    baby = models.ForeignKey(
        'Baby',
        on_delete=models.CASCADE,
        related_name='retina_prints'
    )
    image_path = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RetinaPrint for {self.baby} uploaded at {self.uploaded_at}"