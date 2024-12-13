from django.core.exceptions import ValidationError
from django.template import TemplateSyntaxError

from utils.constants import TEMPLATE_LOAD_TAGS
from utils.render_template_from_string import template_from_string


def validate_template_content(value):
    try:
        template = template_from_string(TEMPLATE_LOAD_TAGS + value)
    except TemplateSyntaxError as e:
        raise ValidationError(e.args[0].get("chain"))
