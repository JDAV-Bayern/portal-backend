from django import template
from babel.numbers import format_currency

register = template.Library()


def currency(value):
    if value is None:
        return ""
    return format_currency(value, "EUR", locale="de_DE")

def distance(value):
    if value is None:
        return ""
    return f"{value:.0f} km"


register.filter('currency', currency)
register.filter('distance', distance)
