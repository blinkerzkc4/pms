from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from user.choices import UserTypeChoices


def validate_main_admin_for_vendor_properties(user_type):
    if user_type != UserTypeChoices.ADMIN:
        raise ValidationError(
            _("Only Admin users are allowed to be main admin in the properties.")
        )
    return user_type
