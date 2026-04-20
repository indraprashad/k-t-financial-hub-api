from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from common.permissions import IsAdminOrReadOnly
from .models import BlogCategory
from .serializers import BlogCategorySerializer


class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name']
    ordering_fields = ['name', 'created_at']
