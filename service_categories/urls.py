from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceCategoryViewSet

router = DefaultRouter()
router.register(r'service-categories', ServiceCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
