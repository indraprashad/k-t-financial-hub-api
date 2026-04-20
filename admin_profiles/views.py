from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from common.permissions import IsAdminOrReadOnly
from .models import AdminProfile
from .serializers import AdminProfileSerializer


class AdminProfileViewSet(viewsets.ModelViewSet):
    queryset = AdminProfile.objects.all().order_by('-created_at')
    serializer_class = AdminProfileSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['role']
    ordering_fields = ['created_at', 'role']

    @action(detail=False, methods=['get', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Get or update current user's admin profile."""
        profile, created = AdminProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'email': request.user.email,
                'name': request.user.get_full_name() or request.user.username,
            }
        )

        if request.method == 'PATCH':
            serializer = self.get_serializer(profile, data=request.data, partial=True, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        serializer = self.get_serializer(profile, context={'request': request})
        return Response(serializer.data)
