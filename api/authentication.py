import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from .models import User

SECRET_KEY = '123456'

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            raise AuthenticationFailed("Authorization header is missing")
        
        if not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Authorization header must start with 'Bearer '")

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f"Invalid token: {e}")

        try:
            user = User.objects.get(id=payload['id'])
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")

        return (user, token)


