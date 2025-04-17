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




    
