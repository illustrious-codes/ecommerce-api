from django.shortcuts import get_object_or_404
from rest_framework.generics import views
from yaml import serialize

from order import serializers
from utils.utility import send_otp
from .serializers import ForgetPasswordSerializer, SignUpUserSerializer, LoginUserSerializer, verifyOTPSerializer, ResetPasswordSerializer
from rest_framework import status, mixins, viewsets, generics, decorators
from rest_framework.response import Response
from.models import User
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404


class SignUpUserAPI(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = SignUpUserSerializer
    permission_classes = [AllowAny]

    # def get_queryset(self):
    #     user = User.objects.get(user=self.request.user.profile)
    #     return user


class LonginUserApi(views.APIView):
    # queryset = User.objects.all()
    serializer_class = LoginUserSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(request_body=LoginUserSerializer)
    def post(self, req):
        serializer = self.serializer_class(data=req.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data
        data = {
            "id":user_data['user'].id,
            "first_name": user_data['user'].first_name,
            "last_name": user_data['user'].last_name,
            "email": user_data['user'].email,
            "username": user_data['user'].username,
            "phone": user_data['user'].phone,
            "is_verified": user_data['user'].is_verified,
            "date_joined": user_data['user'].date_joined,  
            "token": user_data['token']  
        }
        return Response(data)

class AuthenticationViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = None
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'verify_otp':
            return verifyOTPSerializer
        elif self.action == "forget_password":
            return ForgetPasswordSerializer
        elif self.action == "reset_password":
            return ResetPasswordSerializer
        return super().get_serializer_class()
    
    @decorators.action(methods=['post'], detail=False, url_path='verify-otp')
    def verify_otp(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response({"message": "Your account have been verified"})
        return Response(serializer.error)
    
    @decorators.action(methods=["post"], detail=False, url_path="get-otp")
    def get_otp(self, request):
        _= request.data.get("type")
        email = request.data.get("email")
        user = get_object_or_404(User, email__iexact=email)

        if user.is_verified:
            return Response({"message": "Your account has already been verifield"})
        type_ = _.replace("_", " ")

        send_otp(user, email, type_)
        return Response({"message": "OTP has been sent to your email"})
    
    @decorators.action(methods=["post"], detail=False, url_path="forget-password")
    def forget_password(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "otp sent to your mail"})
        return Response({"message": serializer.error})
    
    @decorators.action(methods=["post"], detail=False, url_path="reset-password")
    def reset_password(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Your password has been reset'})
        return Response({'message': serializer.error})