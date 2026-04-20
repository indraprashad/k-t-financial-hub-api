from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from common.permissions import IsAdminOrReadOnly
from .models import ServicesContent
from .serializers import ServicesContentSerializer


class ServicesContentViewSet(viewsets.ModelViewSet):
    queryset = ServicesContent.objects.all()
    serializer_class = ServicesContentSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['service_id', 'category', 'content_type']
    ordering_fields = ['item_index', 'created_at', 'title']
