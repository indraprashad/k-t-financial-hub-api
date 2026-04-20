import base64
import os
import uuid
from datetime import datetime
from django.conf import settings
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import HomeContent


class HomeContentSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    # Writable fields
    content_type = serializers.ChoiceField(choices=HomeContent.CONTENT_TYPES, write_only=True)
    item_index = serializers.IntegerField(write_only=True)
    title = serializers.CharField(required=False, allow_blank=True, write_only=True)
    heading = serializers.CharField(required=False, allow_blank=True, write_only=True)
    subtitle = serializers.CharField(required=False, allow_blank=True, write_only=True)
    description = serializers.CharField(required=False, allow_blank=True, write_only=True)
    text = serializers.CharField(required=False, allow_blank=True, write_only=True)
    label = serializers.CharField(required=False, allow_blank=True, write_only=True)
    value = serializers.CharField(required=False, allow_blank=True, write_only=True)
    trust_badge = serializers.ListField(child=serializers.DictField(child=serializers.CharField()), required=False, write_only=True)
    icon = serializers.CharField(required=False, allow_blank=True, write_only=True)
    image = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)

    class Meta:
        model = HomeContent
        fields = ['id', 'type', 'attributes', 'content_type', 'item_index', 'title', 'heading', 'subtitle', 'description', 'text', 'label', 'value', 'trust_badge', 'icon', 'image']

    def validate(self, data):
        content_type = data.get('content_type')

        if content_type == 'stat':
            # Stat requires label, value, and icon
            if not data.get('label'):
                raise serializers.ValidationError({'label': 'Label is required for stat content'})
            if not data.get('value'):
                raise serializers.ValidationError({'value': 'Value is required for stat content'})
            if not data.get('icon'):
                raise serializers.ValidationError({'icon': 'Icon is required for stat content'})
            # Clear other fields for stat
            data['title'] = ''
            data['heading'] = ''
            data['subtitle'] = ''
            data['description'] = ''
            data['text'] = ''

        elif content_type == 'hero':
            # Hero should not have label and value
            data['label'] = ''
            data['value'] = ''

        return data

    def get_type(self, obj):
        return 'home'

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
            return {
                'id': obj.id,
                'type': 'home-image',
                'attributes': {
                    'url': url
                }
            }
        return None

    def get_attributes(self, obj):
        return {
            'content_type': obj.content_type,
            'title': obj.title,
            'heading': obj.heading,
            'subtitle': obj.subtitle,
            'description': obj.description,
            'text': obj.text,
            'label': obj.label,
            'value': obj.value,
            'trust_badge': obj.trust_badge or [],
            'icon': obj.icon,
            'image': self.get_image(obj),
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
                    filename = f"home_{instance.id}_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
                    file_path = os.path.join('home_images', filename)
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
                    # Remove file from filesystem
                    import os
                    from django.conf import settings
                    file_path = os.path.join(settings.MEDIA_ROOT, instance.image)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                instance.image = None
            else:
                # Update image
                self._process_image(instance, image_data)
        return super().update(instance, validated_data)
