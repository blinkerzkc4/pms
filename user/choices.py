from django.db.models import TextChoices


class UserTypeChoices(TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    ADMIN = "ADMIN", "Admin"
    MUNICIPALITY_USER = "MUNICIPALITY_USER", "Municipality User"
    WARD_USER = "WARD_USER", "Ward User"


class RoleLevelChoices(TextChoices):
    MUNICIPALITY = "municipality", "Municipality"
    WARD = "ward", "Ward"
    DEPARTMENT = "department", "Department"


class DataSizeChoices(TextChoices):
    MB = "MB", "Megabyte"
    GB = "GB", "Gigabyte"


class StatusChoices(TextChoices):
    SUSPENDED = "SUSPENDED", "Suspended"
    ACTIVE = "ACTIVE", "Active"
    PENDING = "PENDING", "Pending"
