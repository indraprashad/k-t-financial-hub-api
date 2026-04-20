from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsultationBookingViewSet

router = DefaultRouter()
router.register(r'consultation-bookings', ConsultationBookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
