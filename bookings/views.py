from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.conf import settings
from common.permissions import IsAdminOrReadOnly
from common.email_templates import render_consultation_email
from .models import ConsultationBooking
from .serializers import ConsultationBookingSerializer


class ConsultationBookingViewSet(viewsets.ModelViewSet):
    queryset = ConsultationBooking.objects.all()
    serializer_class = ConsultationBookingSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['service', 'preferred_date']
    ordering_fields = ['-created_at', 'preferred_date']

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    def perform_create(self, serializer):
        booking = serializer.save()
        self.send_booking_notification(booking)

    def send_booking_notification(self, booking):
        admin_email = getattr(settings, 'ADMIN_NOTIFICATION_EMAIL', settings.DEFAULT_FROM_EMAIL)

        subject = f'📅 New Consultation Booking - {booking.name}'
        html_message = render_consultation_email(booking)

        send_mail(
            subject=subject,
            message='',  # Plain text fallback
            from_email=admin_email,
            recipient_list=[admin_email],
            fail_silently=True,
            html_message=html_message,
        )
