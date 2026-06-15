from django.db import transaction

from cdr22.models import Compra, CompraItem, Proveedor


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
