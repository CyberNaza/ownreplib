from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import CustomUser, VerificationCode
import random   
from django.utils.translation import gettext_lazy as _
from .utils import send_verification_email
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework.exceptions import AuthenticationFailed

class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'full_name', 'is_active',
            'is_staff', 'is_worker', 'is_admin', 'is_verified',
        ]
        read_only_fields = [
            'id', 'email', 'is_active', 'is_staff',
            'is_worker', 'is_admin', 'is_verified',
        ]

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

        code = f"{random.randint(100000, 999999)}"
        VerificationCode.objects.create(user=user, code=code)
        send_verification_email(user.email, code)
        # In real app: send this code via email or SMS
        print(f"Verification code for {user.email}: {code}")

        return user
    


from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()
from rest_framework.exceptions import AuthenticationFailed
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer to use email as the login field
    """
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        
        if email is None:
            raise serializers.ValidationError(_('This field may not be null.'), code='required')
        if password is None:
            raise serializers.ValidationError(_('This field may not be null.'), code='required')

        # Check if user exists
        try:
            user_obj = User.objects.get(email=email)
            if not user_obj.is_verified:
                raise AuthenticationFailed(_('Please verify your account via the verification code sent to your email.'), code='authorization')
        except User.DoesNotExist:
            pass  # Avoid leaking that the email exists

        # Try to authenticate
        user = authenticate(self.context['request'], email=email, password=password)
        
        if user is None:
            raise AuthenticationFailed(_('Unable to log in with provided credentials.'), code='authorization')

        data = super().validate(attrs)

        # Include user details in the response
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_worker': user.is_worker,
            'is_admin': user.is_admin,
            'is_verified': user.is_verified,
        }

        return data



from rest_framework import serializers
from .models import VerificationCode, CustomUser

class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")

        try:
            verification = user.verification_code
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError("No verification code found for this user.")

        if verification.code != code:
            raise serializers.ValidationError("Invalid verification code.")

        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        print(f"Before: is_verified = {user.is_verified}")
        user.is_verified = True
        user.save()
        print(f"After: is_verified = {user.is_verified}")
        user.verification_code.delete()
        return user



from rest_framework import serializers
from .models import Comment, Like, CustomUser
from library.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email']

class LikeSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Like
        fields = ['id', 'owner', 'liked_at', 'comment']


class CommentSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'owner', 'text', 'created_at', 'updated_at', 'likes']

    def get_likes(self, obj):
        return LikeSerializer(Like.objects.filter(comment=obj), many=True).data
