from django import template


register = template.Library()


@register.filter
def get_field_value(request, field_name):
    return getattr(request, field_name, None)
