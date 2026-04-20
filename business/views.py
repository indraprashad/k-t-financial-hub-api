from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from common.permissions import IsAdminOrReadOnly
from .models import BusinessContact
from .serializers import BusinessContactSerializer


class BusinessContactViewSet(viewsets.ModelViewSet):
    queryset = BusinessContact.objects.all()
    serializer_class = BusinessContactSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['content_type', 'item_index']
    ordering_fields = ['item_index', 'created_at']
