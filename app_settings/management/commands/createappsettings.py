from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from app_settings.models import AppSettingCollection
from project.models import Municipality
from user.models import Client


class Command(BaseCommand):
    help = "Creates app settings in the specified client database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--client_db",
            action="store",
            dest="client_db",
            help="Database to create app settings into.",
        )

    def create_app_settings(self, database):
        self.stdout.write(f"Creating app settings for {database}...")

        if database == "default" or database == settings.SUPERUSER_DOMAIN:
            self.stdout.write(
                self.style.ERROR(
                    "App settings cannot be created in the default database."
                )
            )
            return

        client = Client.objects.get(subdomain=database)

        municipality = (
            Municipality.objects.using(database)
            .filter(code=client.municipality.code)
            .first()
        )
        if not municipality:
            return self.stdout.write(
                self.style.ERROR(
                    f"Municipality with id {client.municipality_id} does not exist in {database}"
                )
            )

        if (
            AppSettingCollection.objects.using(database)
            .filter(municipality=municipality)
            .exists()
        ):
            self.stdout.write(
                self.style.WARNING(
                    f"App settings already exist for {database}. Skipping creation and updating app settings..."
                )
            )
            call_command("updateappsettings", client_db=database)
            return

        AppSettingCollection.objects.using(database).create(municipality=municipality)

        self.stdout.write(
            self.style.SUCCESS(f"App settings for {database} created successfully")
        )

        self.stdout.write(
            self.style.HTTP_INFO(f"Updating app settings for {database}...")
        )

        call_command("updateappsettings", client_db=database)

    def handle(self, *args, **options):
        if options["client_db"]:
            self.create_app_settings(options["client_db"])
        else:
            for database in settings.DATABASES.keys():
                self.create_app_settings(database)
