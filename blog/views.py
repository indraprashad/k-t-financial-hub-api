from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from common.permissions import IsAdminOrReadOnly
from .models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'published', 'featured']
    search_fields = ['title', 'excerpt', 'body']
    ordering_fields = ['created_at', 'published_at', 'title']

    def get_queryset(self):
        queryset = super().get_queryset()
        category_name = self.request.query_params.get('category_name')
        if category_name:
            queryset = queryset.filter(category__name__iexact=category_name)
        return queryset
