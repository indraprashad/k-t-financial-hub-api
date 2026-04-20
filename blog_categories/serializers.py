from rest_framework import serializers
from .models import BlogCategory


class BlogCategorySerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    name = serializers.CharField(write_only=True, required=True)
    description = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = BlogCategory
        fields = ['id', 'type', 'attributes', 'name', 'description']

    def get_type(self, obj):
        return 'blog_category'

    def get_attributes(self, obj):
        return {
            'name': obj.name,
            'slug': obj.slug,
            'description': obj.description,
            'created_at': obj.created_at,
            'updated_at': obj.updated_at,
        }

    def create(self, validated_data):
        name = validated_data.pop('name', '')
        description = validated_data.pop('description', None)
        return BlogCategory.objects.create(name=name, description=description)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
