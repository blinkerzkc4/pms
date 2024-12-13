import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from user.models import Client


class Command(BaseCommand):
    help = "Command to generate the URLs file of the clients."

    def handle(self, *args, **options):
        self.stdout.write("Generating URLs file of the clients...")
        client_urls = list(Client.objects.active().values_list("subdomain", flat=True))
        client_urls_file = os.path.join(settings.CONFIGS_DIR, "client_urls.json")
        with open(client_urls_file, "w") as f:
            json.dump(client_urls, f, indent=4)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully generated URLs file of the clients at {client_urls_file}."
            )
        )
