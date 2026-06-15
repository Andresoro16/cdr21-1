from decimal import Decimal, InvalidOperation

from django import template


register = template.Library()


@register.filter
def money(value):
    try:
        amount = Decimal(value or 0)
    except (InvalidOperation, TypeError, ValueError):
        amount = Decimal(0)

    formatted = f"{amount:,.2f}"
    formatted = formatted.replace(",", "TEMP").replace(".", ",").replace("TEMP", ".")
    return f"$ {formatted}"
