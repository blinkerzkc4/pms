from django.db import router


def get_db_alias(instance):
    return router.db_for_read(instance.__class__, instance=instance)
