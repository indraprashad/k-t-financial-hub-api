from django.db import models
from common.models import BaseModel


class ContactSubmission(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, null=True, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'
