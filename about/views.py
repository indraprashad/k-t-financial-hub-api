from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from common.permissions import IsAdminOrReadOnly
from .models import AboutContent
from .serializers import AboutContentSerializer


class AboutContentViewSet(viewsets.ModelViewSet):
    queryset = AboutContent.objects.all()
    serializer_class = AboutContentSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['content_type', 'item_index']
    ordering_fields = ['item_index', 'created_at']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['delete'], permission_classes=[IsAdminOrReadOnly])
    def delete_image(self, request, pk=None):
        """Delete the image associated with this about content."""
        instance = self.get_object()
        if instance.image:
            # Remove file from filesystem if it's a stored file
            if not instance.image.startswith('data:'):
                import os
                from django.conf import settings
                file_path = os.path.join(settings.MEDIA_ROOT, instance.image)
                if os.path.exists(file_path):
                    os.remove(file_path)
            instance.image = None
            instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
