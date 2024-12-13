import datetime
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from app_settings.models import AppSettingCollection
from base_model.models import BaseModel
from user.choices import RoleLevelChoices, StatusChoices
from utils.csv_import.client_details import ClientDetails


class PermissionManager(models.Manager):
    def user_permissions(self, user):
        if user.is_superuser:
            return self.all()
        return self.filter(granted_roles__users=user).distinct()


class Permission(BaseModel):
    level = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    name_eng = models.CharField(max_length=255, null=True, blank=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    objects = PermissionManager()

    def __str__(self):
        return f"{self.level} {self.name_eng}"

    class Meta:
        ordering = ("level",)

    @property
    def is_child(self):
        return self.parent is not None


class UserRole(BaseModel):
    municipality = models.ForeignKey(
        "project.Municipality", on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=255)

    permissions = models.ManyToManyField(
        Permission, related_name="granted_roles", blank=True
    )

    status = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        unique_together = (
            "municipality",
            "title",
        )
        ordering = (
            "municipality",
            "title",
        )

    def __str__(self):
        return self.title


def digital_signature_name(instance, filename: str):
    ext = filename.split(".")[-1]
    file_name = f"{uuid.uuid5(uuid.NAMESPACE_DNS, instance.email)}.{ext}"
    return f"digital_signatures/{file_name}"


class User(AbstractUser):
    role_level = models.CharField(
        max_length=20,
        choices=RoleLevelChoices.choices,
        default=RoleLevelChoices.MUNICIPALITY,
    )
    eoffice_reference_code = models.CharField(max_length=255, blank=True, null=True)
    notification_room_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )

    assigned_ward = models.ForeignKey(
        "project.Ward", on_delete=models.PROTECT, null=True, blank=True
    )
    assigned_municipality = models.ForeignKey(
        "project.Municipality", on_delete=models.PROTECT, null=True, blank=True
    )
    assigned_department = models.ForeignKey(
        "employee.Department", on_delete=models.PROTECT, null=True, blank=True
    )
    verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        upload_to="profile_picture/", null=True, blank=True
    )
    detail = models.TextField(blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    ip_address = models.CharField(max_length=100, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    user_role = models.ManyToManyField(UserRole, related_name="users", blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)
    digital_signature = models.ImageField(
        upload_to=digital_signature_name, null=True, blank=True
    )
    is_digital_signature_verified = models.BooleanField(default=False, blank=True)
    digital_signature_verification_token = models.UUIDField(
        null=True, blank=True, editable=False
    )

    @property
    def has_signature(self):
        return self.digital_signature is not None

    def save(self, *args, **kwargs) -> None:
        if self.id:
            if not self.digital_signature:
                self.is_digital_signature_verified = False
                self.digital_signature_verification_token = None
            if self.digital_signature and not self.is_digital_signature_verified:
                self.digital_signature_verification_token = uuid.uuid4()
            if self.digital_signature and self.is_digital_signature_verified:
                self.digital_signature_verification_token = None
        return super().save(*args, **kwargs)


class ExternalUser(models.Model):
    external_app_name = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    linked_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="external_user",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "External User"
        verbose_name_plural = "External Users"


class ClientManager(models.Manager):
    def active(self):
        return self.filter(status=StatusChoices.ACTIVE)


class Client(BaseModel):
    client_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    municipality = models.OneToOneField(
        "project.Municipality",
        related_name="client",
        on_delete=models.CASCADE,
        unique=True,
    )
    main_admin = models.OneToOneField(
        "user.User",
        on_delete=models.PROTECT,
        related_name="client_details",
        null=True,
        blank=True,
    )
    valid_till = models.DateField(default=timezone.now, blank=True, null=True)
    database_host = models.GenericIPAddressField(protocol="IPv4", default="172.19.0.24")
    database_name = models.CharField(max_length=255)
    database_user = models.CharField(max_length=255)
    database_password = models.CharField(max_length=255)
    database_port = models.CharField(max_length=4, default="5432")
    subdomain = models.CharField(
        max_length=255, default="yojana.lgerp.org", unique=True
    )
    eservice_url = models.CharField(
        max_length=255, default="eservice.pms.lgerp.org", null=True, blank=True
    )

    objects = ClientManager()
    client_details = ClientDetails.create()

    status = models.CharField(
        max_length=20,
        blank=True,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
    )

    @property
    def active(self):
        return self.valid_till >= datetime.date.today()

    def save(self, *args, **kwargs):
        if not self.client_id:
            client_id = self.client_details.get_client_details_by_address_mapping_code(
                self.municipality.code
            )["client_id"].values
            if len(client_id) > 0:
                self.client_id = client_id[0]
        return super().save(*args, **kwargs)

    @property
    def logo(self):
        app_setting_collection = self.municipality.app_setting_collections
        if app_setting_collection:
            return (
                app_setting_collection.image_app_settings.filter(
                    code="municipality_logo"
                )
                .first()
                .setting_value
            )
        return None

    def __str__(self) -> str:
        return f"{self.municipality} - {self.subdomain}"


@receiver(post_save, sender=Client)
def create_app_setting_collection(sender, instance, created, **kwargs):
    if created:
        AppSettingCollection.objects.create(municipality=instance.municipality)


@receiver(post_save, sender=ExternalUser)
def create_user(sender, instance: ExternalUser, created, **kwargs):
    if created:
        user = User.objects.create_superuser(
            username=instance.username,
            email=f"{instance.external_app_name}@pms.lgerp.org",
            password=instance.password,
        )
        user.verified = True
        user = user.save()
        instance.linked_user = user
        instance.save()
