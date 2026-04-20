from django.db import models
from common.models import BaseModel


class ConsultationBooking(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    service = models.CharField(max_length=255)
    preferred_date = models.DateField()
    message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Consultation Booking'
        verbose_name_plural = 'Consultation Bookings'
