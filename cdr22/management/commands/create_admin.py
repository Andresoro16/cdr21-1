from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help='Crea un super administrador'
    
    def add_arguments(self, parser):
        parser.add_argument('nombre', type=str, help='Nombre')
        parser.add_argument('email', type=str, help='Email')
        parser.add_argument('password', type=str, help='Password')
    
    def handle(self, *args, **options):
        nombre = options['nombre']
        email=options['email']
        password=options['password']
        self.stdout.write(self.style.SUCCESS(f'Admin {nombre} con email {email} con password {password}'))