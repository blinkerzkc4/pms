norms_display = [
    # ("id", "ID"),
    ("activity_no", "Activity No."),
    ("specification_no", "Spec Cl No."),
    ("description_eng", "Description Of Work"),
    ("description", "विवरण"),
    ("unit_display", "Unit"),
    (
        lambda x: x["labour_component"][0]["category"]["title"]
        if x["labour_component"]
        else "",
        "Work Force Type",
    ),
    (
        lambda x: x["labour_component"][0]["unit_representation"]["name"]
        or x["labour_component"][0]["unit_representation"]["name_eng"]
        if x["labour_component"]
        else "",
        "Work Force Unit",
    ),
    (
        lambda x: x["labour_component"][0]["quantity"] if x["labour_component"] else "",
        "Work Force Quantity",
    ),
    (
        lambda x: x["labour_component"][0]["amount"] if x["labour_component"] else "",
        "Work Force Amount",
    ),
    (
        lambda x: x["material_component"][0]["category"]["title"]
        if x["material_component"]
        else "",
        "Material Type",
    ),
    (
        lambda x: x["material_component"][0]["unit_representation"]["name"]
        or x["material_component"][0]["unit_representation"]["name_eng"]
        if x["material_component"]
        else "",
        "Material Unit",
    ),
    (
        lambda x: x["material_component"][0]["quantity"]
        if x["material_component"]
        else "",
        "Material Quantity",
    ),
    (
        lambda x: x["material_component"][0]["amount"]
        if x["material_component"]
        else "",
        "Material Amount",
    ),
    (
        lambda x: x["equipment_component"][0]["category"]["title"]
        if x["equipment_component"]
        else "",
        "Equipment Type",
    ),
    (
        lambda x: x["equipment_component"][0]["unit_representation"]["name"]
        or x["equipment_component"][0]["unit_representation"]["name_eng"]
        if x["equipment_component"]
        else "",
        "Equipment Unit",
    ),
    (
        lambda x: x["equipment_component"][0]["quantity"]
        if x["equipment_component"]
        else "",
        "Equipment Quantity",
    ),
    (
        lambda x: x["equipment_component"][0]["amount"]
        if x["equipment_component"]
        else "",
        "Equipment Amount",
    ),
]

district_rate_display = [
    # ("id", "ID"),
    ("topic", "Description"),
    ("topic_unicode", "विवरण"),
    ("unit", "Unit"),
    ("source", "Source"),
    ("area", "Area"),
    (
        lambda x: x["rate_1"]["amount"]
        if isinstance(x["rate_1"], dict)
        else x["rate_1"],
        "Rate 1",
    ),
    (
        lambda x: x["rate_1"]["fy"] if isinstance(x["rate_1"], dict) else "",
        "Rate 1 Year",
    ),
    (
        lambda x: x["rate_2"]["amount"]
        if isinstance(x["rate_2"], dict)
        else x["rate_2"],
        "Rate 2",
    ),
    (
        lambda x: x["rate_2"]["fy"] if isinstance(x["rate_2"], dict) else "",
        "Rate 2 Year",
    ),
    (
        lambda x: x["rate_3"]["amount"]
        if isinstance(x["rate_3"], dict)
        else x["rate_3"],
        "Rate 3",
    ),
    (
        lambda x: x["rate_3"]["fy"] if isinstance(x["rate_3"], dict) else "",
        "Rate 3 Year",
    ),
]
