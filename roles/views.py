import secrets
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework import viewsets, filters, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from common.permissions import IsAdminOrReadOnly, IsSuperAdmin
from .email_templates import render_invitation_email
from .models import Role, UserRole, Invitation
from .serializers import RoleSerializer, UserRoleSerializer, InvitationSerializer


def ensure_default_roles():
    """Ensure only super_admin and admin roles exist"""
    Role.objects.get_or_create(
        name='super_admin',
        defaults={
            'description': 'Full system access and control',
            'permissions': ['create', 'read', 'update', 'delete', 'manage_users', 'manage_roles']
        }
    )
    Role.objects.get_or_create(
        name='admin',
        defaults={
            'description': 'Administrative access with content management',
            'permissions': ['create', 'read', 'update', 'delete']
        }
    )


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Role.objects.all().order_by('name')
    serializer_class = RoleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        ensure_default_roles()
        return Role.objects.filter(name__in=['super_admin', 'admin']).order_by('name')


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all().order_by('-created_at')
    serializer_class = UserRoleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'role']
    search_fields = ['user__username', 'role__name']
    ordering_fields = ['created_at']


class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all().order_by('-created_at')
    serializer_class = InvitationSerializer
    permission_classes = [IsSuperAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_accepted']
    search_fields = ['email']
    ordering_fields = ['created_at', 'expires_at']

    def perform_create(self, serializer):
        role_id = self.request.data.get('role_id')
        email = self.request.data.get('email')

        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            raise serializers.ValidationError({'role_id': 'Role not found'})

        # Check if invitation already exists for this email
        existing_invitation = Invitation.objects.filter(email=email, is_accepted=False).first()
        if existing_invitation:
            # Resend existing invitation with new token and expiration
            existing_invitation.token = secrets.token_urlsafe(32)
            existing_invitation.expires_at = timezone.now() + timedelta(days=7)
            existing_invitation.role = role
            existing_invitation.invited_by = self.request.user
            existing_invitation.save()
            self.send_invitation_email(existing_invitation)
            raise serializers.ValidationError({
                'detail': 'Invitation already exists. A new invitation email has been sent.',
                'invitation_id': existing_invitation.id
            })

        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(days=7)

        invitation = serializer.save(
            email=email,
            role=role,
            invited_by=self.request.user,
            token=token,
            expires_at=expires_at
        )

        self.send_invitation_email(invitation)

    def send_invitation_email(self, invitation):
        invitation_url = f"{self.request.build_absolute_uri('/').rstrip('/')}/api/invitations/accept/?token={invitation.token}"

        subject = "You're Invited to Join K&T Financial! 🎉"
        html_message = render_invitation_email(invitation, invitation_url)

        send_mail(
            subject=subject,
            message='',  # Plain text fallback
            from_email='noreply@ktfinancial.com',
            recipient_list=[invitation.email],
            fail_silently=False,
            html_message=html_message,
        )

    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='verify')
    def verify(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            invitation = Invitation.objects.get(token=token, is_accepted=False)
            if invitation.expires_at < timezone.now():
                return Response({'error': 'Invitation has expired'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'valid': True,
                'email': invitation.email,
                'role': invitation.role.name,
            })
        except Invitation.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='accept')
    def accept(self, request):
        token = request.data.get('token')
        password = request.data.get('password')
        username = request.data.get('username')

        if not all([token, password, username]):
            return Response(
                {'error': 'Token, username, and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            invitation = Invitation.objects.get(token=token, is_accepted=False)
            if invitation.expires_at < timezone.now():
                return Response({'error': 'Invitation has expired'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(
                username=username,
                email=invitation.email,
                password=password,
                is_staff=True
            )

            UserRole.objects.create(user=user, role=invitation.role)

            invitation.is_accepted = True
            invitation.accepted_at = timezone.now()
            invitation.save()

            return Response({
                'message': 'Invitation accepted successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': invitation.role.name,
                }
            })
        except Invitation.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
