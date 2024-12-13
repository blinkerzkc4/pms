import csv
import json


class FEDERAL_TYPES:
    COUNTRY = "1"
    PROVINCE = "2"
    DISTRICT = "3"
    RURAL_MUNICIPALITY = "4"
    MUNICIPALITY = "5"
    SUB_METROPOLITAN = "6"
    METROPOLITAN = "7"


def get_federal_types_from_csv():
    federal_types = []
    with open(
        "./prefill_data/FederalType.csv", "r", encoding="utf-8-sig"
    ) as federal_types_csv:
        reader = csv.DictReader(federal_types_csv)
        for row in reader:
            federal_types.append(
                {
                    "id": row["id"],
                    "code": row["code"],
                    "name": row["name_np"],
                    "name_eng": row["name_en"],
                    "name_unicode": row["name_np"],
                    "upper_level_type_id": row["upper_level_type_id"],
                }
            )
    return federal_types


def get_addresses_from_csv():
    with open(
        "./prefill_data/Address Details.csv", "r", encoding="utf-8-sig"
    ) as addresses_csv:
        reader = csv.DictReader(addresses_csv)
        provinces = []
        districts = []
        municipalities = []
        others = []
        for row in reader:
            if row["federal_level_type_id"] == FEDERAL_TYPES.PROVINCE:
                provinces.append(row)
            elif row["federal_level_type_id"] == FEDERAL_TYPES.DISTRICT:
                districts.append(row)
            elif row["federal_level_type_id"] in [
                FEDERAL_TYPES.RURAL_MUNICIPALITY,
                FEDERAL_TYPES.MUNICIPALITY,
                FEDERAL_TYPES.SUB_METROPOLITAN,
                FEDERAL_TYPES.METROPOLITAN,
            ]:
                municipalities.append(row)
            else:
                others.append(row)
    return {
        "provinces": provinces,
        "districts": districts,
        "municipalities": municipalities,
        "others": others,
    }


def get_modules_from_csv():
    with open(
        "./prefill_data/ModuleType.csv", "r", encoding="utf-8-sig"
    ) as modules_csv:
        reader = csv.DictReader(modules_csv)
        modules = []
        for row in reader:
            modules.append(row)
        return modules


def get_chart_of_accounts_from_csv():
    with open(
        "./prefill_data/ChartofAccount.csv", "r", encoding="utf-8-sig"
    ) as chart_of_accounts_csv:
        reader = csv.DictReader(chart_of_accounts_csv)
        chart_of_accounts = []
        for row in reader:
            chart_of_accounts.append(row)
        return chart_of_accounts


def main():
    addresses = get_addresses_from_csv()
    with open("./test_data/addresses.json", "w") as addresses_json:
        json.dump(addresses, addresses_json, indent=4)
    federal_types = get_federal_types_from_csv()
    with open("./test_data/federal_types.json", "w") as federal_types_json:
        json.dump(federal_types, federal_types_json, indent=4)


if __name__ == "__main__":
    main()
