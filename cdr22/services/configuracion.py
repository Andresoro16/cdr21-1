from django.db import transaction

from cdr22.models import ConfiguracionSistema, Factura


def get_configuracion_sistema():
    configuracion, _ = ConfiguracionSistema.objects.get_or_create(
        pk=1,
        defaults={
            'siguiente_numero_factura': Factura.objects.count() + 1,
        }
    )
    return configuracion


def generar_numero_factura():
    with transaction.atomic():
        configuracion, _ = ConfiguracionSistema.objects.select_for_update().get_or_create(
            pk=1,
            defaults={
                'siguiente_numero_factura': Factura.objects.count() + 1,
            }
        )

        numero = f"{configuracion.prefijo_factura}-{configuracion.siguiente_numero_factura:06d}"
        while Factura.objects.filter(numero=numero).exists():
            configuracion.siguiente_numero_factura += 1
            numero = f"{configuracion.prefijo_factura}-{configuracion.siguiente_numero_factura:06d}"

        configuracion.siguiente_numero_factura += 1
        configuracion.save(update_fields=['siguiente_numero_factura', 'updated_at'])

    return numero
