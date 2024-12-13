def get_relation_id(data: dict, key: str):
    id_from_data = None
    value_from_data = data.get(key)
    if not (isinstance(value_from_data, int) or isinstance(value_from_data, str)):
        if value_from_data is not None:
            if isinstance(value_from_data, dict):
                id_from_data = value_from_data.get("id")
            else:
                id_from_data = value_from_data.id
    return id_from_data
