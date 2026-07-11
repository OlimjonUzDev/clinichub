from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number']

    def create(self, validated_data):
        validated_data['role'] = 'patient'
        return User.objects.create_user(**validated_data)
    
    def validate_password(self, value):
        validate_password(value)
        return value
    
    password = serializers.CharField(write_only=True)
