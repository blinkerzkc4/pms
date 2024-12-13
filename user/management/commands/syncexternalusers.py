from django.conf import settings
from django.core.management.base import BaseCommand

from user.models import ExternalUser


class Command(BaseCommand):
    help = "Command to sync external users with across all databases"

    def handle(self, *args, **options):
        databases = settings.DATABASES.keys()

        central_db_external_users = ExternalUser.objects.all()

        external_users = [
            ExternalUser(
                external_app_name=external_user.external_app_name,
                username=external_user.username,
                password=external_user.password,
            )
            for external_user in central_db_external_users
        ]

        for database in databases:
            self.stdout.write(
                self.style.SUCCESS(f"Syncing external users for {database}")
            )
            if database == "default" or database == settings.SUPERUSER_DOMAIN:
                continue

            database_external_users = ExternalUser.objects.using(database).all()

            non_existing_external_users = [
                external_user
                for external_user in external_users
                if not database_external_users.filter(
                    external_app_name=external_user.external_app_name
                ).exists()
            ]

            ExternalUser.objects.using(database).bulk_create(
                non_existing_external_users
            )

        self.stdout.write(
            self.style.SUCCESS(
                "External users synced successfully across all databases"
            )
        )
