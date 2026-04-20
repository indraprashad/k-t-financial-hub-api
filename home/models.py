from django.db import models
from common.models import BaseModel


class HomeContent(BaseModel):
    CONTENT_TYPES = [
        ('hero', 'Hero'),
        ('stat', 'Stat'),
    ]

    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES)
    item_index = models.IntegerField(default=0)
    title = models.CharField(max_length=255, null=True, blank=True)
    heading = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    trust_badge = models.JSONField(default=list, blank=True)
    icon = models.CharField(max_length=100, null=True, blank=True, help_text="Icon name for stat items (lucide-react icon names)")
    image = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['item_index', 'created_at']
        verbose_name = 'Home Content'
        verbose_name_plural = 'Home Contents'
