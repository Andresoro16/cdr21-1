from django.db import transaction

from cdr22.models import Compra, CompraItem, Proveedor


class CompraEstadoError(Exception):
    def __init__(self, errores):
        self.errores = errores
        super().__init__("No se pudo cambiar el estado de la compra")


def crear_compra(data):
    proveedor = data.get('proveedor')
    proveedor_nombre = data.get('proveedor_nombre', '').strip()
    items = data['items']
    impuesto = data.get('impuesto') or 0

    subtotal = sum(item['subtotal'] for item in items)
    total = subtotal + impuesto

    with transaction.atomic():
        if proveedor is None and proveedor_nombre:
            proveedor = Proveedor.objects.create(nombre=proveedor_nombre)

        compra = Compra.objects.create(
            proveedor=proveedor,
            numero_factura=data.get('numero_factura', ''),
            fecha_compra=data['fecha_compra'],
            subtotal=subtotal,
            impuesto=impuesto,
            total=total,
            metodo_pago=data.get('metodo_pago') or None,
            estado=data['estado'],
            observaciones=data.get('observaciones', ''),
        )

        for item in items:
            CompraItem.objects.create(
                compra=compra,
                producto=item['producto'],
                cantidad=item['cantidad'],
                costo_unitario=item['costo_unitario'],
                subtotal=item['subtotal'],
            )

        if compra.estado == 'completada':
            compra.aplicar_stock()

    return compra


def cambiar_estado_compra(compra, nuevo_estado):
    transiciones_permitidas = {
        'borrador': ['en_espera', 'completada', 'anulada'],
        'en_espera': ['borrador', 'completada', 'anulada'],
        'completada': [],
        'anulada': [],
    }

    if nuevo_estado == compra.estado:
        return compra

    if nuevo_estado not in dict(Compra.ESTADO_CHOICES):
        raise CompraEstadoError({
            'estado': ['Seleccione un estado válido.']
        })

    estados_destino = transiciones_permitidas.get(compra.estado, [])
    if nuevo_estado not in estados_destino:
        raise CompraEstadoError({
            'estado': [f'No se puede cambiar una compra de {compra.get_estado_display()} a {dict(Compra.ESTADO_CHOICES)[nuevo_estado]}.']
        })

    if nuevo_estado == 'anulada':
        return anular_compra(compra)

    with transaction.atomic():
        compra.estado = nuevo_estado
        compra.save(update_fields=['estado', 'updated_at'])

        if compra.estado == 'completada':
            compra.aplicar_stock()

    return compra


def anular_compra(compra, motivo=''):
    if compra.estado == 'completada':
        raise CompraEstadoError({
            'estado': ['No se puede anular una compra completada porque ya aplicó stock.']
        })

    if compra.estado == 'anulada':
        raise CompraEstadoError({
            'estado': ['Esta compra ya está anulada.']
        })

    with transaction.atomic():
        compra.anular(motivo=motivo)

    return compra
