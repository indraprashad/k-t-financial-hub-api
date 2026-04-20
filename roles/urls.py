from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, UserRoleViewSet, InvitationViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'user-roles', UserRoleViewSet)
router.register(r'invitations', InvitationViewSet, basename='invitation')

urlpatterns = [
    path('', include(router.urls)),
]
