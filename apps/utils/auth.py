from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
import jwt
from apps.users.models import Users
from django.conf import settings


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_token = request.META.get("HTTP_AUTHTOKEN", "")
        try:
            payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        except (jwt.DecodeError, jwt.InvalidSignatureError):
            raise exceptions.AuthenticationFailed("Invalid token")
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')
        email = payload.get("email")
        user = Users.objects.filter(email=email).first()

        if not user:
            raise exceptions.AuthenticationFailed('Unauthenticated')

        return user, None
