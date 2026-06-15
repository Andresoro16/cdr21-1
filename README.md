## Ejecucion del servidor en local

- Abrir una terminal dentro del proyecto
- ejecutar `.\venv\Scripts\activate`
- ejecutar `pip install -r requirements.txt`
- ejecutar ` python manage.py tailwind start`
- Abrimos otra terminal
- ejecutar `python manage.py runserver`
- Abrir en el navegador la URL que nos da el ultimo comando.

## Ejecucion local con Docker

Construir y levantar Django:

```bash
docker compose up --build web
```

Aplicar migraciones:

```bash
docker compose exec web python manage.py migrate
```

Crear superusuario:

```bash
docker compose exec web python manage.py createsuperuser
```

Levantar Tailwind en modo watcher, si se van a tocar estilos:

```bash
docker compose --profile frontend up tailwind
```

El servicio web queda disponible en:

```text
http://localhost:8000
```

Si Mailpit esta corriendo en la maquina host, el contenedor usa `host.docker.internal:1025`.

## Produccion
- python manage.py tailwind build

## Produccion con Docker / Coolify

Archivos de produccion:

```text
Dockerfile.prod
docker-compose.prod.yml
docker/nginx/default.conf
scripts/post-deploy.sh
```

En Coolify, usar `docker-compose.prod.yml` y publicar el servicio `nginx` en el puerto interno `80`.

Variables minimas recomendadas:

```env
DJANGO_DEBUG=False
SECRET_KEY=valor-seguro
ALLOWED_HOSTS=midominio.com,www.midominio.com
CSRF_TRUSTED_ORIGINS=https://midominio.com,https://www.midominio.com
```

Despues de cada deploy, ejecutar dentro del servicio `web`:

```bash
./scripts/post-deploy.sh
```

Ese script corre:

```bash
python manage.py migrate --noinput
python manage.py tailwind build
python manage.py collectstatic --noinput
```

Por ahora produccion usa SQLite persistente en el volumen `cdr22-data` y archivos subidos en `cdr22-media`.

## Cambios para las variables CSS

## Tests E2E con Playwright

Para ejecutar tests automatizados con Playwright:

```bash
# En Terminal 1: Inicia el servidor Django
python manage.py runserver

# En Terminal 2: Ejecuta los tests
python tests_e2e/login.py
python tests_e2e/crear_producto.py
python tests_e2e/crear_cliente.py
```

Los scripts generan **screenshots automáticos** en `tests_e2e/screenshots/` para evidencia de funcionalidad.

### Usar Playwright Codegen (para crear nuevos tests)

```bash
python -m playwright codegen http://localhost:8000
```

Se abrirá un navegador interactivo donde puedes:
- Hacer clic en elementos
- Rellenar formularios
- El código se genera automáticamente en el panel derecho

## Comandos

### Agregar Stock

```bash
python manage.py add_stock --sku "PROD-001" --cantidad 50
python manage.py add_stock --id 5 --cantidad 30
```
