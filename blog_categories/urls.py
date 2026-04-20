from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogCategoryViewSet

router = DefaultRouter()
router.register(r'blog-categories', BlogCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
