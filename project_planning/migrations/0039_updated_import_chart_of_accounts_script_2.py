from django.db import migrations, models

from project_planning.models import (
    AccountTitleManagement as AccountTitleManagementModel,
)
from project_planning.models import SubModule as SubModuleModel
from utils.import_csv_data import get_chart_of_accounts_from_csv, get_modules_from_csv
from utils.search import search_list_of_dicts


def populate_account_title_management_model(apps, schema_editor):
    modules_data = get_modules_from_csv()
    chart_of_accounts_data = get_chart_of_accounts_from_csv()
    AccountTitleManagement: AccountTitleManagementModel = apps.get_model(
        "project_planning", "AccountTitleManagement"
    )
    SubModule: SubModuleModel = apps.get_model("project_planning", "SubModule")
    db_alias = schema_editor.connection.alias
    AccountTitleManagement.objects.using(db_alias).all().delete()
    for chart_of_account in chart_of_accounts_data:
        try:
            int(chart_of_account["code"])
        except ValueError:
            continue
        atm, updated = AccountTitleManagement.objects.using(db_alias).update_or_create(
            code=chart_of_account["code"],
            defaults={
                "name": chart_of_account["name_np"],
                "name_eng": chart_of_account["name_en"],
                "transfer_account": chart_of_account["is_transfer_acc"] == "t",
                "is_transactable": chart_of_account["is_transactable"] == "t",
                "fund_account": chart_of_account["is_fund_acc"] == "t",
                "base_account": chart_of_account["is_base_account"] == "t",
                "is_budgeted": chart_of_account["is_budgetable"] == "t",
                "remarks": chart_of_account["remarks"],
                "sapati": chart_of_account["is_sapati"] == "t",
                "capital_ratio": chart_of_account["capital_ratio"],
                "current_ratio": chart_of_account["current_ratio"],
            },
        )
        if chart_of_account.get("parent_id"):
            try:
                parent_atm, created = AccountTitleManagement.objects.using(
                    db_alias
                ).get_or_create(
                    code=search_list_of_dicts(
                        chart_of_accounts_data, "id", chart_of_account["parent_id"]
                    )["code"]
                )
                atm.parent = parent_atm
            except AccountTitleManagement.MultipleObjectsReturned:
                parent_atm = (
                    AccountTitleManagement.objects.using(db_alias)
                    .filter(
                        code=search_list_of_dicts(
                            chart_of_accounts_data, "id", chart_of_account["parent_id"]
                        )["code"]
                    )
                    .first()
                )
                atm.parent = parent_atm
            atm.save()
        if chart_of_account.get("module_type"):
            module = SubModule.objects.using(db_alias).filter(
                code=search_list_of_dicts(
                    modules_data, "id", chart_of_account["module_type"]
                )["code"]
            )
            if module.exists():
                atm.module = module.first()
                atm.save()
        if chart_of_account.get("sub_module_id"):
            sub_module = SubModule.objects.using(db_alias).filter(
                code=search_list_of_dicts(
                    modules_data, "id", chart_of_account["sub_module_id"]
                )["code"]
            )
            if sub_module.exists():
                atm.sub_module = sub_module.first()
                atm.save()
        print(
            f"Account title management {atm.name} created with code {atm.code}", end=""
        )
        if atm.parent:
            print(f" with parent {atm.parent.name} (Code: {atm.parent.code})")
        else:
            print()


class Migration(migrations.Migration):
    dependencies = [
        ("project_planning", "0038_updated_import_chart_of_accounts_script"),
    ]

    operations = [
        migrations.RunPython(populate_account_title_management_model),
    ]
