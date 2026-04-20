import base64
import os
import uuid
from datetime import datetime
from django.conf import settings
from rest_framework import serializers
from .models import ServicesContent


class ServicesContentSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField(read_only=True)

    # Writable fields
    image = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)

    class Meta:
        model = ServicesContent
        fields = ['id', 'type', 'attributes', 'service_id', 'category', 'content_type', 'title', 'description', 'tagline', 'features', 'image', 'item_index']

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

    def get_type(self, obj):
        return 'service'

    def get_attributes(self, obj):
        return {
            'service_id': obj.service_id,
            'category': obj.category.id if obj.category else None,
            'category_name': obj.category.name if obj.category else None,
            'content_type': obj.content_type,
            'title': obj.title,
            'description': obj.description,
            'tagline': obj.tagline,
            'features': obj.features,
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
                    filename = f"service_{instance.id}_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
                    file_path = os.path.join('service_images', filename)
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
                if instance.image and not instance.image.startswith('data:'):
                    file_path = os.path.join(settings.MEDIA_ROOT, instance.image)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                instance.image = None
            else:
                self._process_image(instance, image_data)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return {
            'id': str(instance.id),
            'type': 'service',
            'attributes': {
                'service_id': instance.service_id,
                'category': instance.category.id if instance.category else None,
                'category_name': instance.category.name if instance.category else None,
                'content_type': instance.content_type,
                'title': instance.title,
                'description': instance.description,
                'tagline': instance.tagline,
                'features': instance.features,
                'image': self.get_image(instance),
                'item_index': instance.item_index,
                'created_at': instance.created_at,
                'updated_at': instance.updated_at,
            }
        }
