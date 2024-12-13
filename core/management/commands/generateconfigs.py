from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Command to refresh the server."

    def handle(self, *args, **options):
        self.stdout.write("Generating config files...")
        call_command("generateclienturls")
        call_command("generatedbconfigs")
        call_command("generatenginxconfig")
        self.stdout.write(self.style.SUCCESS("Successfully generated config files."))
