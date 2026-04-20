from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HomeContentViewSet

router = DefaultRouter()
router.register(r'home-content', HomeContentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
