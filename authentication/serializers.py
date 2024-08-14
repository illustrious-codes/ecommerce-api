from dataclasses import fields
import email
from os import read
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from .models import User
from rest_framework.authtoken.models import Token
from django.core import exceptions

class SignUpUserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)
    confirm_password = serializers.CharField(write_only=True, max_length=30)
    class Meta:
        model: User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone",
            "email",
            "password",
            "confirm_password",
            "date_joined",
            "is_verifield",
            "Token"
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
            validate_password(password==password) and validate_password(password=confirm_password)
        except exceptions.ValidationError as e:
            errors["password"] = list[e.message]
        email_ = User.objects.filter(email_iexact=email)
        if email_.exists:
            errors["email"] = ["Email already exists"]
        if errors:
            raise serializers.ValidationError(errors)
        return data
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        token = Token.objects.create(user=user)
        self.token = str(token)
        return user