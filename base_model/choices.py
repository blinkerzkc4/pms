from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class VerificationStatusChoices(TextChoices):
    na = "na", _("Not Applicable")
    not_submitted = "not_submitted", _("Not Submitted")
    pending = "pending", _("Pending")
    accepted = "accepted", _("Accepted")
    req_revision = "req_revision", _("Requires Revision")
    rejected = "rejected", _("Rejected")
