import csv
from os import replace


def process_csv(csv_data: str):
    permissions = []

    # Read CSV data
    csv_reader = csv.reader(csv_data.splitlines())
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        level, name, code, english_name, nepali_name = row[:5]
        is_base_level = level.count(".") == 0

        if [level, name, code, english_name, nepali_name] == [""] * 5:
            continue

        # Create a dictionary for the current permission
        permission = {
            "level": level.strip().replace(" ", ""),
            "name": name.strip(),
            "code": code.strip(),
            "english_name": english_name.strip(),
            "nepali_name": nepali_name.strip(),
        }
        if is_base_level:
            permission["parent_code"] = None
        else:
            permission["parent_code"] = level[: level.rfind(".")]
        permissions.append(permission)

    # Sort the permissions by level
    permissions.sort(key=lambda p: p["level"])

    return permissions


if __name__ == "__main__":
    with open("data/permissions/permissions.csv", "r", encoding="utf-8") as f:
        csv_data = f.read()
        permissions = process_csv(csv_data)
        print(permissions)
