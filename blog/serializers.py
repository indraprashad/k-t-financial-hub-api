import base64
import os
import uuid
from datetime import datetime
from django.conf import settings
from rest_framework import serializers
from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    type = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField(read_only=True)

    # Writable fields
    image = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'type', 'attributes', 'category_id', 'title', 'slug', 'excerpt', 'body', 'image', 'published', 'featured']

    def get_type(self, obj):
        return 'blog'

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
            'title': obj.title,
            'slug': obj.slug,
            'excerpt': obj.excerpt,
            'body': obj.body,
            'image': self.get_image(obj),
            'published': obj.published,
            'published_at': obj.published_at,
            'featured': obj.featured,
            'category': obj.category.id if obj.category else None,
            'category_name': obj.category.name if obj.category else None,
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
                    filename = f"blog_{instance.id}_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
                    file_path = os.path.join('blog_images', filename)
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

    def validate_category_id(self, value):
        if value is None:
            return None
        from blog_categories.models import BlogCategory
        try:
            return BlogCategory.objects.get(pk=value)
        except BlogCategory.DoesNotExist:
            raise serializers.ValidationError(f"Category with id {value} does not exist.")

    def create(self, validated_data):
        image_data = validated_data.pop('image', None)
        validated_data['category'] = validated_data.pop('category_id', None)
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
        if 'category_id' in validated_data:
            instance.category = validated_data.pop('category_id')
        return super().update(instance, validated_data)
