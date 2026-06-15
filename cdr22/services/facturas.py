from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from weasyprint import HTML

from cdr22.services.configuracion import get_configuracion_sistema


def render_factura_pdf(orden, base_url=None):
    html = render_to_string(
        'dashboard/facturas/pdf.html',
        {
            'orden': orden,
            'factura': orden.factura,
            'cliente': orden.cliente,
            'items': orden.items.all(),
            'configuracion': get_configuracion_sistema(),
        }
    )

    return HTML(string=html, base_url=base_url).write_pdf()


def enviar_factura_por_email(orden, base_url=None):
    if not orden.cliente or not orden.cliente.email:
        raise ValueError('La venta no tiene un cliente con correo electrónico.')

    pdf = render_factura_pdf(orden, base_url=base_url)
    factura = orden.factura
    asunto = f"Factura {factura.numero}"
    cuerpo = (
        f"Hola {orden.cliente.nombre},\n\n"
        f"Adjuntamos la factura {factura.numero} por tu compra.\n\n"
        f"Gracias."
    )

    email = EmailMessage(
        subject=asunto,
        body=cuerpo,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[orden.cliente.email],
    )
    email.attach(f"factura-{factura.numero}.pdf", pdf, 'application/pdf')
    email.send(fail_silently=False)
