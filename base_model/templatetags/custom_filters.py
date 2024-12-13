from django import template
from django.utils.safestring import mark_safe

from utils.nepali_nums import nepali_nums
from utils.number2words import number_in_words

register = template.Library()


@register.filter
def custom_filter(obj, arg):
    try:
        print(getattr(obj, arg))
        value = getattr(obj, arg)
        return value if value is not None else "-"
    except:
        return "-"


@register.filter()
def nepali_num_converter(num):
    return nepali_nums(num)


@register.filter()
def get_percentage(value, arg):
    try:
        return f"{(value/arg)*100:.2f}%"
    except:
        return "-"


@register.filter()
def in_words(value):
    return number_in_words(value)


@register.filter()
def create_table(related_objs, table_properties_string):
    def get_object_field(obj, field):
        try:
            if "." in field:
                field, sub_field = field.split(".")
                return get_object_field(getattr(obj, field), sub_field)
            else:
                return getattr(obj, field)
        except:
            return "&nbsp;"

    table_propertes = [
        tuple(table_property_string.split(" ", 1))
        for table_property_string in table_properties_string.split(",")
    ]
    table_fields, table_headers = zip(*table_propertes)
    table_header_html = f'<tr><th>{"</th><th>".join(table_headers)}</th></tr>'
    table_body_html = ""
    if related_objs:
        for obj in related_objs.all():
            table_data = [
                str(nepali_nums(get_object_field(obj, field))) for field in table_fields
            ]
            table_data = [data if data != "None" else "&nbsp;" for data in table_data]
            table_body_html += f"<tr><td>{'</td><td>'.join(table_data)}</td></tr>"
    table_html = f'<table style="width:100%;border: 1px solid black;"><thead>{table_header_html}</thead><tbody>{table_body_html}</tbody></table>'
    return mark_safe(table_html)
