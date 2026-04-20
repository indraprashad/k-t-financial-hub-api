from django.db import models
from common.models import BaseModel
from service_categories.models import ServiceCategory


class ServicesContent(BaseModel):
    service_id = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='services'
    )
    content_type = models.CharField(max_length=50, default='service')
    item_index = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    tagline = models.CharField(max_length=255, null=True, blank=True)
    features = models.JSONField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['item_index', 'created_at']
        verbose_name = 'Services Content'
        verbose_name_plural = 'Services Contents'

    def __str__(self):
        return self.title
