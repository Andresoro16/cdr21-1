from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from cdr22.roles import ROLE_NAMES


class Command(BaseCommand):
    help = 'Crea roles iniciales de usuarios'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando seeder de roles...'))

        created_count = 0

        for role_name in ROLE_NAMES:
            _, created = Group.objects.get_or_create(name=role_name)

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Creado: {role_name}'))
            else:
                self.stdout.write(self.style.HTTP_INFO(f'- Ya existe: {role_name}'))

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSeeder completado. Roles creados: {created_count}. Total roles del sistema: {Group.objects.count()}'
            )
        )
