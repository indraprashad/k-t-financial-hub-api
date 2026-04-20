from django.db import models
from django.contrib.auth.models import User
from common.models import BaseModel


class AdminProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    avatar_url = models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    preferences = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = 'Admin Profile'
        verbose_name_plural = 'Admin Profiles'
