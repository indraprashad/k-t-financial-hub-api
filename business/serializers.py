from rest_framework import serializers
from .models import BusinessContact


class BusinessContactSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    content_type = serializers.CharField(write_only=True, required=False, default='contact')
    title = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
    address = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
    phone = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
    email = serializers.EmailField(write_only=True, required=False, allow_null=True, allow_blank=True)
    google_maps_url = serializers.URLField(write_only=True, required=False, allow_null=True, allow_blank=True)
    additional_info = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
    item_index = serializers.IntegerField(write_only=True, required=False, default=0)

    class Meta:
        model = BusinessContact
        fields = ['id', 'type', 'attributes', 'content_type', 'title', 'address', 'phone', 'email', 'google_maps_url', 'additional_info', 'item_index']

    def get_type(self, obj):
        return 'business_contact'

    def get_attributes(self, obj):
        return {
            'content_type': obj.content_type,
            'title': obj.title,
            'address': obj.address,
            'phone': obj.phone,
            'email': obj.email,
            'office_hours': obj.office_hours,
            'google_maps_url': obj.google_maps_url,
            'additional_info': obj.additional_info,
            'item_index': obj.item_index,
            'created_at': obj.created_at,
            'updated_at': obj.updated_at,
        }

    def create(self, validated_data):
        return BusinessContact.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for field in ['content_type', 'title', 'address', 'phone', 'email', 'google_maps_url', 'additional_info', 'item_index']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()
        return instance
