"""
URL configuration for pms_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls.py import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls.py'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="PMS Project",
        default_version="v1",
        description="PMS Project",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


@login_required
def get_error_log_file(request: HttpRequest):
    if not (request.user.is_superuser):
        return Response(
            {"error": "You are not authorized to access this resource"},
            status=status.HTTP_403_FORBIDDEN,
        )
    with open(settings.LOG_FILE, "r") as f:
        error_messages = f.read()
    return render(
        request,
        "error_log.html",
        {"error_messages": error_messages},
    )


urlpatterns = (
    [
        path("error-log/", get_error_log_file),
        path("admin/", admin.site.urls),
        path("api-auth/", include("rest_framework.urls")),
        path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
        path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
        path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
        path("api/user/", include("user.urls")),
        path("api/log/", include("log.urls")),
        path("api/dashboard/", include("dashboard.urls")),
        path("api/", include("project.urls")),
        path("api/", include("employee.urls")),
        path("api/", include("project_planning.urls")),
        path("api/", include("norm.urls")),
        path("api/", include("budget_process.urls")),
        path("api/", include("formulate_plan.urls")),
        path("api/", include("base_model.urls")),
        path("api/", include("plan_execution.urls")),
        path("api/report/", include("pratibedan.urls")),
        path("api/", include("project_report.urls")),
        path("api/notification/", include("notification.urls")),
        path("api/", include("app_settings.urls")),
        path("api/apps_bridge/", include("apps_bridge.urls")),
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        ),
    ]
    + (
        [path("__debug__/", include("debug_toolbar.urls"))]
        if settings.DEBUG_TOOLBAR
        else []
    )
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
