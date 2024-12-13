from django.core.management.base import BaseCommand

from base_model.models import Address
from budget_process.models import BudgetExpenseManagement, BudgetImportLog
from plan_execution.models import BudgetAllocationDetail, ProjectExecution
from project.models import Project


class Command(BaseCommand):
    help = "Command to delete the last imported budget data."

    def handle(self, *args, **options):
        self.stdout.write("Searching for the last imported budget data...")
        last_imported_budget_data = BudgetImportLog.objects.order_by("-id").first()
        if last_imported_budget_data is None:
            self.stdout.write(
                self.style.WARNING(
                    "There is no imported budget data to be deleted. Aborting."
                )
            )
            return
        self.stdout.write(
            self.style.SUCCESS(
                f"Found the last imported budget data with id {last_imported_budget_data.id}."
            )
        )
        self.stdout.write("Deleting the budget allocation details...")
        last_imported_budget_data.imported_budget_allocation_details.all().delete()
        self.stdout.write("Deleting the budget expense management...")
        last_imported_budget_data.imported_budget_expense_management.all().delete()
        self.stdout.write("Deleting the project execution...")
        last_imported_budget_data.imported_project_execution.all().delete()
        self.stdout.write("Deleting the projects...")
        last_imported_budget_data.imported_projects.all().delete()
        self.stdout.write("Deleting the addresses...")
        last_imported_budget_data.imported_addresses.all().delete()
        self.stdout.write("Deleting the budget import log...")
        last_imported_budget_data.delete()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully deleted the last imported budget data with id {last_imported_budget_data.id}."
            )
        )
