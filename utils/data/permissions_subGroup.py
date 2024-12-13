import json


def sub_groupPermissions(permissions: list[str]):
    groups = {}

    for permission in permissions:
        parts = permission.split("_")
        group_key = parts[-1]
        group_name = group_key.title()

        if group_key not in groups:
            groups[group_key] = {
                "subgroup_key": group_key,
                "subgroup_name": group_name,
                "permissions": [],
            }

        groups[group_key]["permissions"].append(permission)

    result = [group for group in groups.values()]
    return result


def main():
    with open("permissions_list.json", "r") as json_file:
        permissions = json.load(json_file)

    sub_grouped_permissions = sub_groupPermissions(permissions)

    sub_groups_keys_list = [group["subgroup_key"] for group in sub_grouped_permissions]

    with open("./permission_subgroups.json", "w", encoding="utf-8") as json_file:
        json.dump(sub_grouped_permissions, json_file, ensure_ascii=False, indent=4)

    with open("./permission_subgroups_keys.json", "w", encoding="utf-8") as json_file:
        json.dump(sub_groups_keys_list, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
