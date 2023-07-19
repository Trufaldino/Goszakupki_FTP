from django import template
from babel.numbers import format_currency


register = template.Library()


@register.filter
def get_field_value(request, field_name):
    return getattr(request, field_name, None)


@register.filter
def space_separated(value):
    try:
        price = float(value)
        formatted_price = format_currency(price, 'RUB', locale='ru_RU', format='#,##0.00')
        return formatted_price
    except (ValueError, TypeError):
        return value
