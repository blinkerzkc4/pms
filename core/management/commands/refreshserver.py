from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Command to refresh the server."

    def handle(self, *args, **options):
        self.stdout.write("Refreshing the server...")
        call_command("load_permissions")
        call_command("createdefaultroles")
        call_command("createclientsuperuser")
        call_command("createappsettings")
        call_command("syncexternalusers")
        self.stdout.write(self.style.SUCCESS("Successfully refreshed the server."))
