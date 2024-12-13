from django.db import migrations, models

from project.models import District as DistrictModel
from project.models import Municipality as MunicipalityModel
from project.models import Province as ProvinceModel
from utils.import_csv_data import get_addresses_from_csv


def update_federal_state_codes(apps, schema_editor):
    federal_addresses = get_addresses_from_csv()
    Province: ProvinceModel = apps.get_model("project", "Province")
    District: DistrictModel = apps.get_model("project", "District")
    Municipality: MunicipalityModel = apps.get_model("project", "Municipality")
    db_alias = schema_editor.connection.alias
    for province in federal_addresses["provinces"]:
        province_model = (
            Province.objects.using(db_alias)
            .filter(name_eng=province["name_en"])
            .first()
        )
        if province_model is not None:
            province_model.code = province["code"]
            province_model.save()
    for district in federal_addresses["districts"]:
        district_model = (
            District.objects.using(db_alias)
            .filter(name_eng=district["name_en"])
            .first()
        )
        if district_model is not None:
            district_model.code = district["code"]
            district_model.save()
    for municipality in federal_addresses["municipalities"]:
        municipality_model = (
            Municipality.objects.using(db_alias)
            .filter(name_eng=municipality["name_en"])
            .first()
        )
        if municipality_model is not None:
            municipality_model.code = municipality["code"]
            municipality_model.save()


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0047_district_code_municipality_code_province_code"),
    ]

    operations = [
        migrations.RunPython(update_federal_state_codes),
    ]
