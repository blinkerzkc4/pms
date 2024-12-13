from django.urls import path

from apps_bridge.views import get_token

app_name = "apps_bridge"
urlpatterns = [
    path("token/", get_token, name="token"),
]
