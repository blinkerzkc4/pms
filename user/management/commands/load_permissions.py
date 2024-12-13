from django.core.management.base import BaseCommand

from django.conf import settings
from user.models import Permission
from utils.permissions_processor import process_csv
from utils.search import search_list_of_dicts


class Command(BaseCommand):
    help = "Command to load permisions from csv file."

    def add_arguments(self, parser):
        parser.add_argument(
            "--database",
            action="store",
            dest="database",
            help="Database to load permissions into.",
        )

    def load_permissions(self, database, permissions):
        self.stdout.write(f"Creating permissions for database of {database}...")
        created_count = 0
        deleted_count = 0

        if database == "default":
            permissions_manager = Permission.objects
        else:
            permissions_manager = Permission.objects.using(database)

        for permission in permissions:
            parent = None
            if permission["parent_code"]:
                parent_permission = search_list_of_dicts(
                    permissions, "level", permission["parent_code"]
                )
                parent, parent_created = permissions_manager.update_or_create(
                    level=permission["parent_code"],
                    defaults={
                        "title": parent_permission["name"],
                        "code": parent_permission["code"],
                        "name_eng": parent_permission["english_name"],
                        "name": parent_permission["nepali_name"],
                    },
                )
            permission_obj, created = permissions_manager.update_or_create(
                level=permission["level"],
                defaults={
                    "title": permission["name"],
                    "code": permission["code"],
                    "name_eng": permission["english_name"],
                    "name": permission["nepali_name"],
                    "parent": parent,
                },
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {created_count} permissions from the csv file from {len(permissions)}. The remaining were already present and updated."
            )
        )

        self.stdout.write(f"Deleting extra permissions for database of {database}...")
        for permission in permissions_manager.all():
            if not search_list_of_dicts(permissions, "level", permission.level):
                permission.delete()
                deleted_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully deleted {deleted_count} permissions from the csv file from {len(permissions)}."
            )
        )

    def handle(self, *args, **options):
        if options["database"]:
            databases = [options["database"]]
        else:
            databases = settings.DATABASES.keys()

        self.stdout.write("Loading permissions from the csv file...")
        with open("data/permissions/permissions.csv", "r", encoding="utf-8") as f:
            csv_data = f.read()
            permissions = process_csv(csv_data)

        self.stdout.write(f"Loaded {len(permissions)} permissions from the csv file.")

        for database in databases:
            self.load_permissions(database, permissions)
