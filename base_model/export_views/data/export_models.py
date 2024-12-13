from base_model.export_views.data.display_fields_and_titles import (
    district_rate_display,
    norms_display,
)
from base_model.export_views.data.model_querysets import (
    get_district_rate_data,
    get_norms_data,
)

export_models = {
    "norms": (
        get_norms_data,
        norms_display,
        "नोर्म",
    ),
    "district-rate": (
        get_district_rate_data,
        district_rate_display,
        "जिल्ला दर",
    ),
}


def get_export_model(export_model_key: str):
    return export_models.get(export_model_key)
