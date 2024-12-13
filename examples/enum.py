from django.db import models


class ProcessStatus(models.TextChoices):
    ACCEPT = "A", "Accept"
    REJECT = "R", "Reject"
    PENDING = "P", "Pending"


if __name__ == "__main__":
    ps = ProcessStatus.PENDING
    psc = ProcessStatus.choices
    short_representation = "P"
    verbose_name = dict(ProcessStatus.choices)[short_representation]
    print(ps, psc, verbose_name)
