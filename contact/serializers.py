from rest_framework import serializers
from .models import ContactSubmission


class ContactSubmissionSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    name = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=True)
    phone = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
    subject = serializers.CharField(write_only=True, required=True)
    message = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = ContactSubmission
        fields = ['id', 'type', 'attributes', 'name', 'email', 'phone', 'subject', 'message']

    def get_type(self, obj):
        return 'contact'

    def get_attributes(self, obj):
        return {
            'name': obj.name,
            'email': obj.email,
            'phone': obj.phone,
            'subject': obj.subject,
            'message': obj.message,
            'created_at': obj.created_at,
            'updated_at': obj.updated_at,
        }

    def create(self, validated_data):
        name = validated_data.pop('name', '')
        email = validated_data.pop('email', '')
        phone = validated_data.pop('phone', None)
        subject = validated_data.pop('subject', '')
        message = validated_data.pop('message', '')
        return ContactSubmission.objects.create(name=name, email=email, phone=phone, subject=subject, message=message)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.message = validated_data.get('message', instance.message)
        instance.save()
        return instance
