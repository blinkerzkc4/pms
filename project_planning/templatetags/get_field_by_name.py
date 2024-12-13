from django import template

register = template.Library()


@register.filter(name="get_val")
def get_val(obj, arg):
    try:
        valu = getattr(obj, arg)
        return f"{valu}"
    except:
        return ""
