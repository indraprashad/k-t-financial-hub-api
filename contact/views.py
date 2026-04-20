from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.conf import settings
from common.permissions import IsAdminOrReadOnly
from common.email_templates import render_contact_email
from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer


class ContactSubmissionViewSet(viewsets.ModelViewSet):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['subject']
    ordering_fields = ['-created_at', 'name']

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    def perform_create(self, serializer):
        submission = serializer.save()
        self.send_contact_notification(submission)

    def send_contact_notification(self, submission):
        admin_email = getattr(settings, 'ADMIN_NOTIFICATION_EMAIL', settings.DEFAULT_FROM_EMAIL)

        subject = f'✉️ New Contact Message - {submission.subject}'
        html_message = render_contact_email(submission)

        send_mail(
            subject=subject,
            message='',  # Plain text fallback
            from_email=admin_email,
            recipient_list=[admin_email],
            fail_silently=True,
            html_message=html_message,
        )
