import base64
import os
import uuid
from datetime import datetime
from django.conf import settings
from rest_framework import serializers
from .models import AboutContent


class AboutContentSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    # Writable fields
    content_type = serializers.ChoiceField(choices=AboutContent.CONTENT_TYPES, write_only=True)
    item_index = serializers.IntegerField(write_only=True)
    heading = serializers.CharField(required=False, allow_blank=True, write_only=True)
    subtitle = serializers.CharField(required=False, allow_blank=True, write_only=True)
    text = serializers.CharField(required=False, allow_blank=True, write_only=True)
    paragraphs = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    name = serializers.CharField(required=False, allow_blank=True, write_only=True)
    role = serializers.CharField(required=False, allow_blank=True, write_only=True)
    bio = serializers.CharField(required=False, allow_blank=True, write_only=True)
    image = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    mission = serializers.CharField(required=False, allow_blank=True, write_only=True)
    vision = serializers.CharField(required=False, allow_blank=True, write_only=True)
    year = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = AboutContent
        fields = [
            'id', 'type', 'attributes',
            'content_type', 'heading', 'subtitle', 'text', 'paragraphs',
            'name', 'role', 'bio', 'image', 'mission', 'vision', 'year',
            'item_index'
        ]

    def get_type(self, obj):
        return 'about'

    def get_image(self, obj):
        if obj.image:
            if obj.image.startswith('data:'):
                url = obj.image
            elif obj.image.startswith('http'):
                url = obj.image
            else:
                request = self.context.get('request')
                if request:
                    url = request.build_absolute_uri(settings.MEDIA_URL + obj.image)
                else:
                    url = settings.MEDIA_URL + obj.image
            return url
        return None

    def get_attributes(self, obj):
        return {
            'content_type': obj.content_type,
            'heading': obj.heading,
            'subtitle': obj.subtitle,
            'text': obj.text,
            'paragraphs': obj.paragraphs,
            'name': obj.name,
            'role': obj.role,
            'bio': obj.bio,
            'image': self.get_image(obj),
            'mission': obj.mission,
            'vision': obj.vision,
            'year': obj.year,
            'item_index': obj.item_index,
            'created_at': obj.created_at,
            'updated_at': obj.updated_at,
        }

    def _process_image(self, instance, image_data):
        if image_data:
            if image_data.startswith('data:'):
                try:
                    format_info, imgstr = image_data.split(';base64,')
                    ext = format_info.split('/')[-1]
                    if ext == 'jpeg':
                        ext = 'jpg'
                    filename = f"about_{instance.id}_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
                    file_path = os.path.join('about_images', filename)
                    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    data = base64.b64decode(imgstr)
                    with open(full_path, 'wb') as f:
                        f.write(data)
                    instance.image = file_path
                except Exception:
                    instance.image = image_data
            else:
                instance.image = image_data
        else:
            instance.image = None

    def create(self, validated_data):
        image_data = validated_data.pop('image', None)
        instance = super().create(validated_data)
        if image_data:
            self._process_image(instance, image_data)
            instance.save()
        return instance

    def update(self, instance, validated_data):
        image_data = validated_data.pop('image', None)
        if image_data is not None:
            if image_data == '' or image_data is None:
                # Delete image
                if instance.image and not instance.image.startswith('data:'):
                    file_path = os.path.join(settings.MEDIA_ROOT, instance.image)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                instance.image = None
            else:
                # Update image
                self._process_image(instance, image_data)
        return super().update(instance, validated_data)
