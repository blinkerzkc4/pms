"""
-- Created by Bikash Saud
-- Created on 2023-08-25
"""

from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register("view", views.NotificationViewSet, basename="notification")

app_name = "notification"

urlpatterns = router.urls
urlpatterns += [
    path("goto/", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]
