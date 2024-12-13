from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from websocket import WebSocket

from notification.models import Notification
from notification.tasks import send_notification as send_notification_task
from utils.db_utils import get_db_alias


@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created and instance.user:
        channel_layer = get_channel_layer()

        room_group_name = f"notification_{instance.user.notification_room_id}"

        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {"type": "notification.message", "notification_id": instance.id},
        )
