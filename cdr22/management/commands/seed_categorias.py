from django.core.management.base import BaseCommand
from cdr22.models import Categoria


class Command(BaseCommand):
    help = 'Crea categorías iniciales para productos'

    def handle(self, *args, **options):
        categorias_data = [
            {
                'nombre': 'Frenos',
                'descripcion': 'Pastillas de freno, discos, tambores y componentes del sistema de frenado'
            },
            {
                'nombre': 'Motor',
                'descripcion': 'Filtros de aceite, aire, bujías, correas y componentes del motor'
            },
            {
                'nombre': 'Suspensión',
                'descripcion': 'Amortiguadores, resortes, bujes y componentes de la suspensión'
            },
            {
                'nombre': 'Transmisión',
                'descripcion': 'Embragues, cajas de cambio, diferenciales y componentes de transmisión'
            },
            {
                'nombre': 'Dirección',
                'descripcion': 'Cremalleras, terminales, rótulas y componentes del sistema de dirección'
            },
            {
                'nombre': 'Sistema Eléctrico',
                'descripcion': 'Baterías, alternadores, arrancadores y componentes eléctricos'
            },
            {
                'nombre': 'Refrigeración',
                'descripcion': 'Radiadores, bombas de agua, termostatos y componentes del sistema de enfriamiento'
            },
            {
                'nombre': 'Escape',
                'descripcion': 'Silenciadores, catalizadores, tubos y componentes del sistema de escape'
            },
            {
                'nombre': 'Carrocería',
                'descripcion': 'Faros, retrovisores, parachoques y componentes de la carrocería'
            },
            {
                'nombre': 'Neumáticos',
                'descripcion': 'Llantas, neumáticos, válvulas y componentes relacionados'
            },
            {
                'nombre': 'Lubricantes',
                'descripcion': 'Aceites de motor, transmisión, hidráulico y otros lubricantes'
            },
            {
                'nombre': 'Herramientas',
                'descripcion': 'Herramientas especializadas para taller automotriz'
            }
        ]

        self.stdout.write(self.style.SUCCESS('Iniciando seeder de categorías...'))
        
        created_count = 0
        updated_count = 0

        for categoria_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nombre=categoria_data['nombre'],
                defaults={'descripcion': categoria_data['descripcion']}
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Creada: {categoria.nombre}')
                )
            else:
                # Actualizar descripción si ya existe
                if categoria.descripcion != categoria_data['descripcion']:
                    categoria.descripcion = categoria_data['descripcion']
                    categoria.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'↻ Actualizada: {categoria.nombre}')
                    )
                else:
                    self.stdout.write(
                        self.style.HTTP_INFO(f'- Ya existe: {categoria.nombre}')
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Seeder completado:\n'
                f'   • Categorías creadas: {created_count}\n'
                f'   • Categorías actualizadas: {updated_count}\n'
                f'   • Total categorías: {Categoria.objects.count()}'
            )
        )