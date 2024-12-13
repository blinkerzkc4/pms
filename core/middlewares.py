from django.conf import settings
from django.http import HttpResponseForbidden
from rest_framework.permissions import SAFE_METHODS


class SuperUserOnlyMiddleware(object):
    NOT_ALLOWED_IN_URLS = ["client", "externaluser"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_domain = request.get_host()

        not_allowed_in_urls = [x in request.path for x in self.NOT_ALLOWED_IN_URLS]

        if (
            any(not_allowed_in_urls)
            and settings.SUPERUSER_DOMAIN not in current_domain
            and request.method not in SAFE_METHODS
        ):
            return HttpResponseForbidden("You are not allowed to access this page.")

        response = self.get_response(request)

        return response


import threading

request_cfg = threading.local()


class DatabaseRouterMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        domain_to_check = request.headers.get(
            "host",
            request.headers.get(
                "referer", request.headers.get("Application-Url", request.get_host())
            ),
        )

        for key, value in settings.DATABASES.items():
            other_urls_check = [
                other_url in domain_to_check
                for other_url in value.get("OTHER_URLS", [])
            ]
            if key in domain_to_check or any(other_urls_check):
                request_cfg.cfg = key
                break

        response = self.get_response(request)

        if hasattr(request_cfg, "cfg"):
            del request_cfg.cfg

        return response


class DatabaseRouter(object):
    default_db_models = {
        "Client",
        "ExternalUser",
    }

    def _default_db(self, model, **hints):
        # for dir_key in dir(model._meta):
        #     if dir_key.startswith("_"):
        #         continue
        #     print(dir_key)
        #     print(getattr(model._meta, dir_key))
        if model._meta.object_name in self.default_db_models:
            return "default"
        if hasattr(request_cfg, "cfg"):
            return request_cfg.cfg
        return None

    def db_for_read(self, model, **hints):
        return self._default_db(model, **hints)

    def db_for_write(self, model, **hints):
        return self._default_db(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
