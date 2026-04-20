from rest_framework import serializers
from .models import ConsultationBooking


class ConsultationBookingSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    name = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=True)
    phone = serializers.CharField(write_only=True, required=True)
    service = serializers.CharField(write_only=True, required=True)
    message = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
    preferred_date = serializers.DateField(write_only=True, required=True)

    class Meta:
        model = ConsultationBooking
        fields = ['id', 'type', 'attributes', 'name', 'email', 'phone', 'service', 'message', 'preferred_date']

    def get_type(self, obj):
        return 'booking'

    def get_attributes(self, obj):
        return {
            'name': obj.name,
            'email': obj.email,
            'phone': obj.phone,
            'service': obj.service,
            'message': obj.message,
            'preferred_date': obj.preferred_date,
            'created_at': obj.created_at,
            'updated_at': obj.updated_at,
        }

    def create(self, validated_data):
        return ConsultationBooking.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for field in ['name', 'email', 'phone', 'service', 'message', 'preferred_date']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()
        return instance
