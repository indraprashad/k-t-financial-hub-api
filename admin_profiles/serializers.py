import base64
import os
import uuid
from datetime import datetime
from django.conf import settings
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import AdminProfile


class AdminProfileSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    # Writable fields for updates
    name = serializers.CharField(required=False, write_only=True)
    bio = serializers.CharField(required=False, allow_blank=True, write_only=True)
    avatar_url = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = AdminProfile
        fields = ['id', 'type', 'attributes', 'name', 'bio', 'avatar_url']

    def get_type(self, obj):
        return 'admin_profile'

    def get_attributes(self, obj):
        return {
            'email': obj.email,
            'name': obj.name,
            'username': obj.user.username if obj.user else None,
            'is_staff': obj.user.is_staff if obj.user else False,
            'role': obj.role,
            'bio': obj.bio,
            'image': self.get_image(obj),
            'created_at': obj.created_at,
            'updated_at': obj.updated_at,
        }

    def get_image(self, obj):
        if obj.avatar_url:
            # Check if avatar_url is a base64 data URL or a file path
            if obj.avatar_url.startswith('data:'):
                # Still base64, return as-is for now
                url = obj.avatar_url
            elif obj.avatar_url.startswith('http'):
                # Already a full URL
                url = obj.avatar_url
            else:
                # It's a relative path, build full URL
                request = self.context.get('request')
                if request:
                    url = request.build_absolute_uri(settings.MEDIA_URL + obj.avatar_url)
                else:
                    url = settings.MEDIA_URL + obj.avatar_url
            return {
                'id': obj.id,
                'type': 'profile-image',
                'attributes': {
                    'url': url
                }
            }
        return None

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.bio = validated_data.get('bio', instance.bio)
        if 'avatar_url' in validated_data:
            avatar_data = validated_data['avatar_url']
            if avatar_data:
                # Check if it's a base64 data URL
                if avatar_data.startswith('data:'):
                    # Parse base64 data and save as file
                    try:
                        format_info, imgstr = avatar_data.split(';base64,')
                        ext = format_info.split('/')[-1]
                        if ext == 'jpeg':
                            ext = 'jpg'
                        # Generate unique filename
                        filename = f"avatar_{instance.id}_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
                        # Save to media directory
                        file_path = os.path.join('avatars', filename)
                        full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                        # Ensure directory exists
                        os.makedirs(os.path.dirname(full_path), exist_ok=True)
                        # Decode and save
                        data = base64.b64decode(imgstr)
                        with open(full_path, 'wb') as f:
                            f.write(data)
                        # Store relative path
                        instance.avatar_url = file_path
                    except Exception:
                        # If parsing fails, store original
                        instance.avatar_url = avatar_data
                else:
                    # It's already a URL or path, store as-is
                    instance.avatar_url = avatar_data
            else:
                instance.avatar_url = None
        instance.save()
        return instance
