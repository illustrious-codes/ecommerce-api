from rest_framework.generics import views
from .serializers import SignUpUserSerializer, LoginUserSerializer
from rest_framework import status, mixins, viewsets, generics
from rest_framework.response import Response
from.models import User
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser


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

# class LoginUserApi(APIView):
#     def post(self, request):
#         serializer = LoginUserSerializer(data=request.data)
#         if serializer.is_valid():
#             return Response(serializer.validated_data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)