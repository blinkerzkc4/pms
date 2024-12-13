import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer
from django.conf import settings
from django.db import router
from requests import head

from notification.models import Notification
from notification.serializers import NotificationSerializer
from user.models import User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))


class NotificationConsumer(JsonWebsocketConsumer):
    def connect(self):
        headers = {
            h_key.decode("utf-8"): h_value.decode("utf-8")
            for h_key, h_value in self.scope["headers"]
        }

        self.client_subdomain = headers.get("host").split(":")[0]

        if self.client_subdomain in settings.DATABASES:
            self.db_alias = self.client_subdomain
        else:
            self.db_alias = "default"

        self.notification_room_id = self.scope["url_route"]["kwargs"][
            "notification_room_id"
        ]

        self.room_name = self.scope["url_route"]["kwargs"]["notification_room_id"]

        self.last_notification_id = None
        self.sent_notifications = set()

        self.room_group_name = f"notification_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "notification.message", "total_notifications": 5},
        )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        pass

    def notification_message(self, event):
        notification_id = event.get("notification_id")
        total_notifications = event.get("total_notifications", 1)

        user = User.objects.using(self.db_alias).get(
            notification_room_id=self.notification_room_id
        )

        if not notification_id:
            notifications = (
                Notification.objects.using(self.db_alias)
                .filter(user=user)
                .order_by("-created_date")[:total_notifications]
            )
        else:
            notifications = (
                Notification.objects.using(self.db_alias)
                .filter(id=notification_id)
                .order_by("-created_date")
            )

        if notifications.exists():
            self.last_notification_id = notifications.first().id

            for notification in list(notifications)[::-1]:
                if notification.id in self.sent_notifications:
                    continue

                self.send_json(
                    {
                        **NotificationSerializer(notification).data,
                        "message": notification.description,
                    }
                )
                self.sent_notifications.add(notification.id)

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
