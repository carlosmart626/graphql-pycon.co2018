import jwt
import logging
from threading import local

from django.utils.deprecation import MiddlewareMixin
from rest_framework.request import Request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.contrib.auth import get_user_model
from django.contrib.auth.middleware import get_user
from django.conf import settings
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework_jwt.settings import api_settings


jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class AuthenticationMiddlewareJWT(MiddlewareMixin):

    def authenticate(self, jwt_value=None):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        from django.core.exceptions import PermissionDenied

        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise PermissionDenied(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise PermissionDenied(msg)
        except jwt.InvalidTokenError:
            raise PermissionDenied("Invalid Token")

        user = self.authenticate_credentials(payload)

        return (user, jwt_value)

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        from django.core.exceptions import PermissionDenied
        User = get_user_model()
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise PermissionDenied(msg)

        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = _('Invalid signature.')
            raise PermissionDenied(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise PermissionDenied(msg)

        return user

    def process_request(self, request):
        assert hasattr(request, 'session')
        user = get_user(request)
        if user.is_authenticated is False:
            if request.META.get('HTTP_AUTHORIZATION', None):
                if len(request.META['HTTP_AUTHORIZATION'].split(" ")) > 1:
                    self.authenticate(
                        request.META['HTTP_AUTHORIZATION'].split(" ")[1])[0]
