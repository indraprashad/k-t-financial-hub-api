from rest_framework import serializers
from .models import ServiceCategory


class ServiceCategorySerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ServiceCategory
        fields = ['id', 'type', 'attributes', 'name', 'slug', 'description']

    def get_type(self, obj):
        return 'service_category'

    def get_attributes(self, obj):
        return {
            'name': obj.name,
            'slug': obj.slug,
            'description': obj.description,
            'created_at': obj.created_at,
            'updated_at': obj.updated_at,
        }

    def to_representation(self, instance):
        return {
            'id': str(instance.id),
            'type': 'service_category',
            'attributes': {
                'name': instance.name,
                'slug': instance.slug,
                'description': instance.description,
                'created_at': instance.created_at,
                'updated_at': instance.updated_at,
            }
        }
