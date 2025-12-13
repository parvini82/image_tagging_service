from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, APIKey


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data['email'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("User account is inactive.")
        self.user = user
        return data


class MaskedAPIKeySerializer(serializers.ModelSerializer):
    masked_key = serializers.SerializerMethodField()

    class Meta:
        model = APIKey
        fields = ['id', 'masked_key', 'created_at', 'last_used_at']
        read_only_fields = ['id', 'created_at', 'last_used_at']

    def get_masked_key(self, obj):
        return f"{obj.prefix}****{obj.key[-4:]}"


class APIKeyCreateSerializer(serializers.ModelSerializer):
    key = serializers.SerializerMethodField()
    masked_key = serializers.SerializerMethodField()

    class Meta:
        model = APIKey
        fields = ['id', 'key', 'masked_key', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_key(self, obj):
        # This will only be set during creation
        return getattr(obj, '_raw_key', None)

    def get_masked_key(self, obj):
        return f"{obj.prefix}****{obj.key[-4:]}"
