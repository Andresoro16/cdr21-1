from django.db import transaction

from cdr22.models import Cliente, Factura, Orden, OrdenItem, Producto
from cdr22.services.configuracion import generar_numero_factura


class OrdenStockError(Exception):
    def __init__(self, errores):
        self.errores = errores
        super().__init__('Stock insuficiente')


def crear_orden_pos(validated_data):
    cliente_data = validated_data['cliente']
    items = validated_data['items']

    with transaction.atomic():
        cliente, created = Cliente.objects.get_or_create(
            cedula=cliente_data['cedula'].strip(),
            defaults={
                'nombre': cliente_data.get('nombre', '').strip(),
                'apellidos': cliente_data.get('apellidos', '').strip(),
                'email': cliente_data.get('email', '').strip(),
                'telefono': cliente_data.get('telefono', '').strip(),
            }
        )

        if not created:
            cliente.nombre = cliente_data.get('nombre', cliente.nombre).strip()
            cliente.apellidos = cliente_data.get('apellidos', cliente.apellidos).strip()
            cliente.email = cliente_data.get('email', cliente.email or '').strip()
            cliente.telefono = cliente_data.get('telefono', cliente.telefono or '').strip()
            cliente.save(update_fields=['nombre', 'apellidos', 'email', 'telefono', 'updated_at'])

        productos = {
            producto.id: producto
            for producto in Producto.objects.select_for_update().filter(
                id__in=[item['producto'].id for item in items]
            )
        }

        for item in items:
            producto = productos[item['producto'].id]
            cantidad = item['cantidad']

            if producto.stock < cantidad:
                raise OrdenStockError({
                    'items': [
                        (
                            f"No hay suficiente stock para {producto.nombre}. "
                            f"Disponible: {producto.stock}, solicitado: {cantidad}."
                        )
                    ]
                })

        factura = Factura.objects.create(
            numero=generar_numero_factura(),
            cliente=cliente,
            subtotal=validated_data['subtotal'],
            impuesto=validated_data['impuesto'],
            total=validated_data['total'],
            metodo_pago=validated_data['metodo_pago'],
            estado='emitida',
        )

        orden = Orden.objects.create(
            cliente=cliente,
            factura=factura,
            metodo_pago=validated_data['metodo_pago'],
            subtotal=validated_data['subtotal'],
            impuesto=validated_data['impuesto'],
            precio_total=validated_data['total'],
            estado='completada',
        )

        for item in items:
            producto = productos[item['producto'].id]
            cantidad = item['cantidad']

            OrdenItem.objects.create(
                orden=orden,
                detalle=producto.nombre,
                precio=item['precio_unitario'],
                cantidad=cantidad,
            )

            producto.stock -= cantidad
            producto.save(update_fields=['stock', 'updated_at'])

    return orden
