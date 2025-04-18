from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'Admin', 'Admin'
        NURSE = 'Nurse', 'Nurse'
        PARENT = 'Parent', 'Parent'

    role = models.CharField(max_length=10, choices=Role.choices)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.username
