from django.db import models
from common.models import BaseModel


class AboutContent(BaseModel):
    CONTENT_TYPES = [
        ('hero', 'Hero'),
        ('team_member', 'Team Member'),
        ('value', 'Value'),
        ('timeline_event', 'Timeline Event'),
    ]

    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES)
    item_index = models.IntegerField(default=0)
    heading = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    paragraphs = models.JSONField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    mission = models.TextField(null=True, blank=True)
    vision = models.TextField(null=True, blank=True)
    year = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        ordering = ['item_index', 'created_at']
        verbose_name = 'About Content'
        verbose_name_plural = 'About Contents'
