from .serializers import SignUpUserSerializer
from rest_framework.generics import views
from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from .models import User
from rest_framework.permissions import AllowAny


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