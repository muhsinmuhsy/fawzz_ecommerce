from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    address = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=100, default='')