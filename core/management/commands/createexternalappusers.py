from django.conf import settings
from django.core.management.base import BaseCommand

from project.models import Municipality
from user.models import Client, ExternalUser, User


class Command(BaseCommand):
    help = "Creates a external app users in the specified client database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--client_db",
            action="store",
            dest="client_db",
            help="Database to create superuser into.",
        )

    def create_external_app_users(self, database_alias):
        self.stdout.write(f"Creating external app users for {database_alias}")
        client = Client.objects.get(subdomain=database_alias)
        municipality = (
            Municipality.objects.using(database_alias)
            .filter(code=client.municipality.code)
            .first()
        )
        for external_app_user in ExternalUser.objects.all():
            if (
                User.objects.using(database_alias)
                .filter(username=external_app_user.username)
                .exists()
            ):
                self.stdout.write(
                    self.style.WARNING(
                        f"External app user for {external_app_user.external_app_name} already exists in {database_alias}. Skipping..."
                    )
                )
                continue
            user = User.objects.using(database_alias).create(
                username=external_app_user.username,
                verified=True,
                is_superuser=True,
                is_staff=True,
                assigned_municipality=municipality,
            )
            user.set_password(external_app_user.password)
            user.save(using=database_alias)
        self.stdout.write(
            self.style.SUCCESS(
                f"External app users for {database_alias} created successfully"
            )
        )

    def handle_single_createexternalappusers(self, client_db):
        DATABASES = settings.DATABASES
        if client_db not in DATABASES.keys():
            self.stdout.write(self.style.ERROR(f"Database {client_db} does not exist"))
            return
        self.create_external_app_users(client_db)

    def handle_createexternalappusers(self):
        DATABASES = settings.DATABASES
        for database_alias, database_config in DATABASES.items():
            if database_alias == "default":
                continue
            self.create_external_app_users(database_alias)

    def handle(self, *args, **options):
        client_db = options["client_db"]
        if client_db:
            self.handle_single_createexternalappusers(client_db)
        else:
            self.handle_createexternalappusers()
