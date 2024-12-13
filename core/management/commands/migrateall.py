from django.core.management.base import BaseCommand
from django.core.management import call_command

from django.conf import settings


class Command(BaseCommand):
    help = "Runs all migrations"

    def handle(self, *args, **options):
        DATABASES = settings.DATABASES
        for database in DATABASES.keys():
            self.stdout.write(f"Running migrations for {database}")
            call_command("migrate", database=database)
            self.stdout.write(
                self.style.SUCCESS(f"Migrations for {database} completed")
            )
