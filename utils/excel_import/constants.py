class QuantityEstimateImportConstants:
    QUANTITY_ESTIMATE_TOPICS_DICT = {
        "S.No.": "s_no",
        "Activity No.": "activity_no",
        "Specification No.": "specification_no",
        "Description": "description",
        "Unit": "unit",
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
        "Type": "quantity_type",
    }

    OLD_QUANTITY_ESTIMATE_TOPICS_DICT = {
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

    STARTING_COL_NAMES = [
        "सि.नं.",
        "सिनं",
        "सि.नं",
        "सिनं.",
        "S.N.",
        "S.N",
        "SN",
        "SN.",
        "S.No.",
        "S.No",
        "SNo",
        "SNo.",
    ]
