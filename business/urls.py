from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessContactViewSet

router = DefaultRouter()
router.register(r'business-contact', BusinessContactViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
