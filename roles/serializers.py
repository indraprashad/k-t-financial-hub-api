from rest_framework import serializers
from .models import Role, UserRole, Invitation


class InvitationSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Invitation
        fields = ['id', 'type', 'attributes']

    def get_type(self, obj):
        return 'invitation'

    def get_attributes(self, obj):
        return {
            'email': obj.email,
            'role': obj.role.name,
            'invited_by': obj.invited_by.username if obj.invited_by else None,
            'token': obj.token,
            'is_accepted': obj.is_accepted,
            'accepted_at': obj.accepted_at,
            'expires_at': obj.expires_at,
            'created_at': obj.created_at,
        }


class RoleSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ['id', 'type', 'attributes']

    def get_type(self, obj):
        return 'role'

    def get_attributes(self, obj):
        return {
            'name': obj.name,
            'description': obj.description,
            'permissions': obj.permissions,
            'created_at': obj.created_at,
            'updated_at': obj.updated_at,
        }


class UserRoleSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = UserRole
        fields = ['id', 'type', 'attributes']

    def get_type(self, obj):
        return 'user_role'

    def get_attributes(self, obj):
        return {
            'user': obj.user.username,
            'role': obj.role.name,
            'created_at': obj.created_at,
            'updated_at': obj.updated_at,
        }
