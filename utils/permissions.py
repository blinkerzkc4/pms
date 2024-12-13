import json


def get_disallowed_permissions():
    with open(
        "utils/data/permissions_disallowed.txt", "r"
    ) as disallowed_permissions_list_file:
        disallowed_permissions_list = (
            disallowed_permissions_list_file.read().splitlines()
        )
    return disallowed_permissions_list


def get_permission_groups():
    with open(
        "utils/data/permission_groups.json", "r", encoding="utf-8"
    ) as permission_groups_file:
        permission_groups = json.load(permission_groups_file)
    return permission_groups


def get_group_of_permission_subgroup(permission_subgroup: str):
    permission_groups = get_permission_groups()
    for group in permission_groups:
        if permission_subgroup in group["sub_groups"]:
            group.pop("sub_groups")
            return group
    return None


def main():
    # print(get_disallowed_permissions())
    print(get_permission_groups())


if __name__ == "__main__":
    main()
