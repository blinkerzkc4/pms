# Generated by Django 4.2.1 on 2023-10-05 00:35

from django.db import migrations, models

from project.models import District as DistrictModel
from project.models import Municipality as MunicipalityModel
from project.models import Province as ProvinceModel
from utils.import_csv_data import get_addresses_from_csv
from utils.search import search_list_of_dicts


def populate_federal_models(apps, schema_editor):
    federal_addresses = get_addresses_from_csv()
    Province: ProvinceModel = apps.get_model("project", "Province")
    District: DistrictModel = apps.get_model("project", "District")
    Municipality: MunicipalityModel = apps.get_model("project", "Municipality")
    db_alias = schema_editor.connection.alias
    Province.objects.using(db_alias).all().delete()
    District.objects.using(db_alias).all().delete()
    Municipality.objects.using(db_alias).all().delete()
    for province in federal_addresses["provinces"]:
        Province.objects.using(db_alias).create(
            name=province["name_np"],
            name_eng=province["name_en"],
            province_number=int(province["id"].split("00")[1]),
        )
    for district_data in federal_addresses["districts"]:
        district_province = Province.objects.using(db_alias).filter(
            name_eng=search_list_of_dicts(
                federal_addresses["provinces"], "id", district_data["parent_id"]
            )["name_en"]
        )
        districts = District.objects.using(db_alias).filter(
            name_eng__icontains=district_data["name_en"]
        )
        if districts.exists():
            district = districts.first()
            if district.province is not None:
                district = districts[1]
            district.name_eng = district_data["name_en"]
            district.name = district_data["name_np"]
            district.province = (
                district_province.first() if district_province.exists() else None
            )
            district.save()
        else:
            District.objects.using(db_alias).create(
                name=district_data["name_np"],
                name_eng=district_data["name_en"],
                province=district_province.first()
                if district_province.exists()
                else None,
            )
    for municipality in federal_addresses["municipalities"]:
        municipality_district = District.objects.using(db_alias).filter(
            name_eng=search_list_of_dicts(
                federal_addresses["districts"], "id", municipality["parent_id"]
            )["name_en"]
        )
        Municipality.objects.using(db_alias).create(
            name=municipality["name_np"],
            name_eng=municipality["name_en"],
            district=municipality_district.first()
            if municipality_district.exists()
            else None,
            number_of_wards=1,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0045_alter_province_options_and_more"),
    ]

    operations = [
        migrations.RunPython(populate_federal_models),
    ]
