from django.db import models
from common.models import BaseModel


class BusinessContact(BaseModel):
    content_type = models.CharField(max_length=50, default='contact')
    item_index = models.IntegerField(default=0)
    title = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    office_hours = models.JSONField(null=True, blank=True)
    google_maps_url = models.URLField(null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['item_index']
        verbose_name = 'Business Contact'
        verbose_name_plural = 'Business Contacts'
