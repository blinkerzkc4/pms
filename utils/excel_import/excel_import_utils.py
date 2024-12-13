import logging

logger = logging.getLogger("Excel Import Utils")


def get_columns_list(topics_dict):
    columns_list = []
    for key, value in topics_dict.items():
        if not isinstance(value, dict):
            columns_list.append(value)
        else:
            for sub_key, sub_value in value["fields"].items():
                columns_list.append(sub_value)
    return columns_list


def get_total_row_span(topics_dict):
    total_row_span = 1
    for key, value in topics_dict.items():
        if isinstance(value, dict):
            total_row_span += 1
    return total_row_span


def get_no_children_snos(dict_keys):
    no_children_snos = []

    for key in dict_keys:
        parent_key = key.rsplit(".", 1)[0]

        if parent_key not in no_children_snos:
            logger.info(f"Parent not found for {key}. Added to no_children_snos.")
            no_children_snos.append(key)
            continue
        elif parent_key in no_children_snos:
            logger.info(
                f"Parent {parent_key} found for {key}. Removed parent from no_children_snos."
            )
            no_children_snos.remove(parent_key)
            no_children_snos.append(key)

    return no_children_snos


def main():
    QUANTITY_ESTIMATE_TOPICS_DICT = {
        "S.No.": "s_no",
        "Activity No.": "activity_no",
        "Specification No.": "specification_no",
        "Description": "description",
        "No.": "no",
        "Description of Quantity": {
            "code": "description_of_quantity",
            "fields": {
                "Length": "length",
                "Breadth": "breadth",
                "Height": "height",
                "Total": "total",
            },
        },
        "Unit": "unit",
    }

    print(get_columns_list(QUANTITY_ESTIMATE_TOPICS_DICT))
    print(get_total_row_span(QUANTITY_ESTIMATE_TOPICS_DICT))


if __name__ == "__main__":
    main()
