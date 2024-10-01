import jwt
from django.conf import settings
from django.http import JsonResponse
from .utils import decode_jwt
from django.contrib.auth.models import User

class JWTAuthenticationMiddleware:
    """Middleware to authenticate users via JWT token."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            try:
                payload = decode_jwt(token.split()[1])
                if payload:
                    request.user = User.objects.get(id=payload['user_id'])
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
                return JsonResponse({'error': 'Invalid token'}, status=401)

        response = self.get_response(request)
        return response
