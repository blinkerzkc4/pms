from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from project.models import Municipality
from user.models import Client, User, UserRole


class Command(BaseCommand):
    help = "Creates a superuser in the specified client database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--client_db",
            action="store",
            dest="client_db",
            help="Database to create superuser into.",
        )

    def handle_single_createsuperuser(self, client_db):
        DATABASES = settings.DATABASES
        if client_db not in DATABASES.keys():
            self.stdout.write(self.style.ERROR(f"Database {client_db} does not exist"))
            return
        self.stdout.write(f"Creating superuser for {client_db}")
        call_command("createsuperuser", database=client_db)
        self.stdout.write(
            self.style.SUCCESS(f"Superuser for {client_db} created successfully")
        )

    def handle_createsuperusers(self):
        DATABASES = settings.DATABASES
        for database_alias, database_config in DATABASES.items():
            if database_alias == "default":
                continue
            client = Client.objects.get(subdomain=database_alias)
            superusers = User.objects.using(database_alias).filter(is_superuser=True)
            admin_role = (
                UserRole.objects.using(database_alias).filter(code="admin").first()
            )
            if superusers.count() > 0:
                self.stdout.write(
                    self.style.WARNING(
                        f"Superuser already exists for {database_alias}. Skipping creation and updating its role..."
                    )
                )

                if not admin_role:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Admin role does not exist for {database_alias}. Skipping updating its role..."
                        )
                    )
                    continue

                for superuser in superusers:
                    superuser.assigned_municipality = client.municipality
                    superuser.save(using=database_alias)
                    superuser.user_role.set([admin_role])
                    superuser.save(using=database_alias)
                continue
            self.stdout.write(f"Creating superuser for {database_alias}")
            municipality = (
                Municipality.objects.using(database_alias)
                .filter(code=client.municipality.code)
                .first()
            )
            if not municipality:
                self.stdout.write(
                    self.style.ERROR(
                        f"Municipality with id {client.municipality_id} does not exist in {database_alias}"
                    )
                )
                continue
            user = User.objects.using(database_alias).create(
                username=database_config["USER"],
                full_name=municipality.name or municipality.name_eng,
                email=client.main_admin.email,
                verified=True,
                is_superuser=True,
                is_staff=True,
                assigned_municipality=municipality,
            )
            user.set_password(database_config["PASSWORD"])
            user.user_role.set([admin_role])
            user.save(using=database_alias)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Superuser for {database_alias} created successfully with username {database_config['USER']} and password {database_config['PASSWORD']}"
                )
            )

    def handle(self, *args, **options):
        client_db = options["client_db"]
        if client_db:
            self.handle_single_createsuperuser(client_db)
        else:
            self.handle_createsuperusers()
