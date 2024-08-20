from re import sub

from django import middleware
from .models import User
from rest_framework.authtoken.models import Token
from django.utils.deprecation import MiddlewareMixin

class UserContextMiddleware(MiddlewareMixin):
    def process_request(self, request):
        header_token = request.META.get("HTTP_AUTHORIZATION", None)

        try:
            if header_token is not None:
                token = sub("Bearer ", "", header_token)
                _token = Token.objects.get(key=token)
                request.user = User.objects.get(id=_token.user_id)
        except (Token.DoesNotExist, User.DoesNotExist):
            request.user = None