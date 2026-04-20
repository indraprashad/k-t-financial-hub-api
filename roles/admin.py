from django.contrib import admin
from .models import Role, UserRole, Invitation


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'role', 'created_at']
    search_fields = ['user__username', 'role__name']
    list_filter = ['role', 'created_at']


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'role', 'invited_by', 'is_accepted', 'expires_at', 'created_at']
    search_fields = ['email', 'role__name', 'invited_by__username']
    list_filter = ['role', 'is_accepted', 'created_at', 'expires_at']
    readonly_fields = ['token', 'accepted_at']
