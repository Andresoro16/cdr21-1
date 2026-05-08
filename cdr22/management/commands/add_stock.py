from django.core.management.base import BaseCommand, CommandError
from cdr22.models import Producto

class Command(BaseCommand):
    help = 'Agrega stock a un producto'
    
    def add_arguments(self, parser):
        parser.add_argument('--sku', type=str, help='SKU del producto')
        parser.add_argument('--id', type=int, help='ID del producto')
        parser.add_argument('--cantidad', type=int, required=True, help='Cantidad a agregar')
    
    def handle(self, *args, **options):
        sku = options.get('sku')
        producto_id = options.get('id')
        cantidad = options.get('cantidad')
        
        # Validar que se proporcione al menos sku o id
        if not sku and not producto_id:
            raise CommandError('Debe proporcionar --sku o --id')
        
        # Buscar el producto
        try:
            if sku:
                producto = Producto.objects.get(sku=sku)
                self.stdout.write(f'Producto encontrado por SKU: {sku}')
            else:
                producto = Producto.objects.get(id=producto_id)
                self.stdout.write(f'Producto encontrado por ID: {producto_id}')
        except Producto.DoesNotExist:
            raise CommandError('El producto no existe')
        
        # Actualizar stock
        stock_anterior = producto.stock
        producto.stock += cantidad
        producto.save()
        
        # Mostrar resumen
        self.stdout.write(self.style.SUCCESS(f'✅ Stock actualizado exitosamente'))
        self.stdout.write(f'Producto: {producto.nombre} ({producto.sku})')
        self.stdout.write(f'Stock anterior: {stock_anterior}')
        self.stdout.write(f'Stock agregado: +{cantidad}')
        self.stdout.write(self.style.SUCCESS(f'Stock nuevo: {producto.stock}'))
