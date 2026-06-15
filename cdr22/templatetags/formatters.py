from decimal import Decimal, InvalidOperation

from django import template

from cdr22.services.configuracion import get_configuracion_sistema


register = template.Library()


@register.filter
def money(value):
    try:
        amount = Decimal(value or 0)
    except (InvalidOperation, TypeError, ValueError):
        amount = Decimal(0)

    formatted = f"{amount:,.2f}"
    formatted = formatted.replace(",", "TEMP").replace(".", ",").replace("TEMP", ".")
    configuracion = get_configuracion_sistema()
    symbol = '$' if configuracion.moneda == 'COP' else configuracion.moneda
    return f"{symbol} {formatted}"
