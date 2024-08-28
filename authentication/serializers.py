from dataclasses import fields
import email
from os import read
from pkg_resources import require
from rest_framework import serializers, generics
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from .models import User
from rest_framework.authtoken.models import Token
from django.core import exceptions
from django.contrib.auth import authenticate
from utils.utility import send_otp
from django.shortcuts import get_object_or_404

class SignUpUserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)
    confirm_password = serializers.CharField(write_only=True, max_length=30)
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "phone",
            "email",
            "password",
            "confirm_password",
            "date_joined",
            "is_verified",
            "token"
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }
        read_only_fields = ["id", "token", "date_joined", "is_verified"]

    
    def validate(self, data):
        errors = {}
        confirm_password = data.get("confirm_password", "")
        password = data.get("password", "")
        email = data.get("email", "")

        if password.lower() != confirm_password.lower():
            errors["password"] = ["password must match"]
        try:
            validate_password(password=password) and validate_password(password=confirm_password)
        except exceptions.ValidationError as e:
            errors["password"] = list[e.messages]
        email_ = User.objects.filter(email__iexact=email)
        if email_.exists():
            errors["email"] = ["Email already exists"]
        if errors:
            raise serializers.ValidationError(errors)
        return data


    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        send_otp(user, validated_data.get('email'), 'Email verification')
        token, _ = Token.objects.get_or_create(user=user)
        self.token = token.key
        return user
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if hasattr(self, "token"):
            data["token"] = self.token
        return data
    
class LoginUserSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(write_only=True)
        token = serializers.CharField(read_only=True)

        def validate(self, data):
            email = data.get('email', '')
            password = data.get('password', '')
            # user = User.objects.filter(email__iexact=email).first()
            if not email and not password:
                raise serializers.ValidationError("Please provide both email and password")
            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("User with this email does not exist")
            
            if not user.check_password(password):
                raise serializers.ValidationError("Password is incorrect")
            
            
            user = authenticate(email=user.email, password=password)

            if not user:
                raise serializers.ValidationError("Authentication failed. Please check your email and password")

            token, _ = Token.objects.get_or_create(user=user)
            data['token'] = token.key
            data['user'] = user
            return data
        
class verifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)

    # def valifate(self, data):
    #     email = data.get("email")
    #     otp = data.get("otp")

    #     user = generics.get_object_or_404(User, email__iexact=email)

    def save(self, **kwargs):
        email = self.validated_data.get("email")
        user = generics.get_object_or_404(User, email__iexact=email)

        if not user.is_verified:
            user.is_verified = True
            user.save()
        return user