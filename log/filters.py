import django_filters

from log.models import AccessLog


class AccessLogFilter(django_filters.FilterSet):
    class Meta:
        model = AccessLog
        fields = (
            "user_id",
            "user_email",
            "username",
            "municipality",
            "ward",
            "actor",
            "path",
            "ip_address",
        )
