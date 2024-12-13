from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Municipality, Ward


@receiver(post_save, sender=Municipality)
def save_profile(sender, instance, created, **kwargs):
    number_of_wards = instance.number_of_wards
    if created:
        wards = [
            Ward(ward_number=i, municipality=instance)
            for i in range(1, number_of_wards + 1)
        ]
        Ward.objects.bulk_create(wards)
    else:
        current_number_of_wards = instance.ward_set.count()
        if current_number_of_wards < number_of_wards:
            wards = [
                Ward(ward_number=i, municipality=instance)
                for i in range(current_number_of_wards + 1, number_of_wards + 1)
            ]
            Ward.objects.bulk_create(wards)
        elif current_number_of_wards > number_of_wards:
            Ward.objects.filter(
                ward_number__gt=number_of_wards, municipality=instance
            ).delete()
