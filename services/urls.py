from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServicesContentViewSet

router = DefaultRouter()
router.register(r'services-content', ServicesContentViewSet)

urlpatterns = [
    path('', include(router.urls)), 
]
