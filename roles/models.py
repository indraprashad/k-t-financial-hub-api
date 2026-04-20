from django.db import models
from django.contrib.auth.models import User
from common.models import BaseModel


class Role(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    permissions = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name


class UserRole(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role_assignment')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users')

    class Meta:
        verbose_name = 'User Role'
        verbose_name_plural = 'User Roles'

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"


class Invitation(BaseModel):
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='invitations')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    token = models.CharField(max_length=100, unique=True)
    is_accepted = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Invitation'
        verbose_name_plural = 'Invitations'

    def __str__(self):
        return f"{self.email} - {self.role.name}"
