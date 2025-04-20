from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove confirmation password
        user = CustomUser(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            date_joined=timezone.now(),
            last_edited=timezone.now(),
            is_active=True,
            is_staff=False,
            is_worker=False,
            is_admin=False
        )
        user.password = make_password(validated_data['password'])
        user.save()
        return user




from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer to use email as the login field
    """
    def validate(self, attrs):
        # Authenticate using the email and password fields
        email = attrs.get("email")
        password = attrs.get("password")
        
        if email is None:
            raise serializers.ValidationError(_('This field may not be null.'), code='required')
        if password is None:
            raise serializers.ValidationError(_('This field may not be null.'), code='required')

        user = authenticate(self.context['request'], email=email, password=password)
        
        if user is None:
            raise serializers.ValidationError(_('Unable to log in with provided credentials.'), code='authorization')
        
        attrs['user'] = user
        return super().validate(attrs)
