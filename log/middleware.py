import logging

from django.http import HttpRequest

from .models import AccessLog

logger = logging.getLogger(__name__)

from django.contrib.auth.middleware import get_user
from django.utils.functional import SimpleLazyObject
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))
        return self.get_response(request)

    @staticmethod
    def get_jwt_user(request):
        user = get_user(request)
        if user.is_authenticated:
            return user
        jwt_authentication = JWTAuthentication()
        try:
            user, token = jwt_authentication.authenticate(request)
        except:
            user = get_user(request)
        return user


class LogMiddleware:
    """
    Middleware for recording access log in the server
    """

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request: HttpRequest, *args, **kwargs):
        # create session
        if not request.session.session_key:
            request.session.create()

        access_log_data = {}
        if request.user.is_authenticated:
            access_log_data["user_id"] = request.user.id
            access_log_data["user_email"] = request.user.email
            access_log_data["username"] = request.user.username
            access_log_data["municipality"] = request.user.assigned_municipality
            access_log_data["ward"] = request.user.assigned_ward
            access_log_data["actor"] = request.user

        # get request path
        access_log_data["path"] = request.path

        # get client's ip address
        x_forwarded_for = request.headers.get("x-forwarded-for")
        access_log_data["ip_address"] = (
            x_forwarded_for.split(",")[0]
            if x_forwarded_for
            else request.META.get("REMOTE_ADDR")
        )
        access_log_data["method"] = request.method
        access_log_data["referer"] = request.headers.get("referer", None)
        access_log_data["session_key"] = request.session.session_key

        data = {}
        data["get"] = dict(request.GET.copy())
        try:
            data["post"] = dict(request.data.copy())
        except:
            data["data"] = dict(request.POST.copy())
        response = self.get_response(request)
        access_log_data["data"] = data
        access_log_data["status_code"] = response.status_code
        try:
            AccessLog.objects.create(**access_log_data)
        except:
            logger.error("Couldn't create access log.")
        return response
