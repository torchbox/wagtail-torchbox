from rest_framework import serializers

class RegistrantSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, max_length=128)
    last_name = serializers.CharField(required=True, max_length=128)
    phone = serializers.CharField(required=True, max_length=20)
    job_title = serializers.CharField(required=True, max_length=128)
    industry = serializers.CharField(required=True, max_length=128)
