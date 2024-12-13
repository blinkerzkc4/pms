from django.urls import re_path

from notification.consumers import ChatConsumer, NotificationConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(
        r"ws/notifications/(?P<notification_room_id>[0-9a-fA-F-]{36})/$",
        NotificationConsumer.as_asgi(),
    ),
]
