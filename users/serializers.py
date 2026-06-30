from rest_framework import serializers

from .models import User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'phone_number']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
