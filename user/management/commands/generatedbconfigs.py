import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from user.models import Client


class Command(BaseCommand):
    help = "Command to generate the database configs file of the clients."

    def handle(self, *args, **options):
        self.stdout.write("Generating database configs file of the clients...")
        database_configs_file = os.path.join(
            settings.CONFIGS_DIR, "database_configs.json"
        )
        database_configs = {}
        for client in Client.objects.active():
            database_configs[client.subdomain] = {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": client.database_name,
                "USER": client.database_user,
                "PASSWORD": client.database_password,
                "HOST": client.database_host,
                "PORT": client.database_port,
                "DISABLE_SERVER_SIDE_CURSORS": True,
                "OTHER_URLS": [client.eservice_url],
            }
        with open(database_configs_file, "w") as f:
            json.dump(database_configs, f, indent=4)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully generated database configs file of the clients at {database_configs_file}."
            )
        )
