from django.conf import settings
from django.core.management.base import BaseCommand

from project.models import Municipality
from user.models import Client, Permission, UserRole


class Command(BaseCommand):
    help = "Command to load permisions from csv file."

    def add_arguments(self, parser):
        parser.add_argument(
            "--database",
            action="store",
            dest="database",
            help="Database to load permissions into.",
        )

    def create_user_roles(self, database_alias):
        client = Client.objects.get(subdomain=database_alias)
        client_municipality = (
            Municipality.objects.using(database_alias)
            .filter(code=client.municipality.code)
            .first()
        )

        if UserRole.objects.using(database_alias).filter(code="admin").exists():
            self.stdout.write(
                self.style.WARNING(
                    f"User role already exists for {database_alias}. Updating its permissions..."
                )
            )
            admin_user_role = UserRole.objects.using(database_alias).get(code="admin")
            admin_user_role.permissions.set(
                Permission.objects.using(database_alias).all()
            )
            admin_user_role.save(using=database_alias)
            self.stdout.write(
                self.style.SUCCESS(
                    f"User role for {database_alias} updated successfully"
                )
            )
            return
        admin_user_role = UserRole.objects.using(database_alias).create(
            title="Admin", code="admin"
        )
        admin_user_role.permissions.set(Permission.objects.using(database_alias).all())
        admin_user_role.municipality = client_municipality
        admin_user_role.save(using=database_alias)
        self.stdout.write(
            self.style.SUCCESS(f"User role for {database_alias} created successfully")
        )

    def handle(self, *args, **options):
        if options["database"]:
            databases = [options["database"]]
        else:
            databases = settings.DATABASES.keys()

        self.stdout.write(f"Creating user roles for {databases}...")

        for database_alias in databases:
            if database_alias == "default":
                continue
            self.create_user_roles(database_alias)

        self.stdout.write(self.style.SUCCESS(f"User roles created successfully"))
