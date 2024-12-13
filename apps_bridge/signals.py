from django.db.models.signals import post_save
from django.dispatch import receiver

from apps_bridge.api_callers.eoffice import EOfficeApi
from user.models import User


@receiver(post_save, sender=User)
def update_eoffice_reference_code(sender, instance, created, **kwargs):
    if created:
        try:
            eoffice_api = EOfficeApi()
        except:
            return
        try:
            eoffice_api.add_user_service(instance)
        except:
            return
