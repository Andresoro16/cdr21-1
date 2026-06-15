# AGENTS.md

Guia para agentes que trabajen en este proyecto. Usar este archivo como mapa inicial antes de modificar codigo.

## Resumen del proyecto

Este es un proyecto Django para gestion tipo POS/inventario/clientes. La app principal del dominio es `cdr22` y la configuracion global del proyecto esta en `config`.

## Tecnologias principales

- Python
- Django 5.2
- Django REST Framework
- django-tailwind
- SQLite para desarrollo local (`db.sqlite3`)

Notas:

- `django-crispy-forms`, `crispy-bootstrap5` y `crispy-tailwind` pueden existir en dependencias, pero no se consideran parte activa del flujo actual. No agregar nuevo trabajo basado en Crispy Forms salvo que se pida explicitamente.
- Playwright fue usado al inicio para pruebas E2E, pero ya no se seguira usando como estrategia principal. No crear nuevos tests con Playwright salvo indicacion explicita.

## Estructura del proyecto

- `manage.py`: entrada principal de comandos Django.
- `config/settings.py`: configuracion global de Django, apps instaladas, base de datos, static files y Tailwind.
- `config/urls.py`: rutas globales del proyecto.
- `cdr22/`: app principal.
- `cdr22/models.py`: modelos del dominio.
- `cdr22/views.py`: vistas HTML tradicionales.
- `cdr22/urls.py`: rutas web de la app.
- `cdr22/api_views.py`: vistas de API.
- `cdr22/api_urls.py`: rutas de API.
- `cdr22/serializers.py`: serializadores de Django REST Framework.
- `cdr22/forms.py`: formularios Django, si se necesitan.
- `cdr22/templates/`: templates de la app.
- `cdr22/templates/components/`: componentes reutilizables de templates.
- `cdr22/static/css/`: CSS propio de la app.
- `cdr22/static/js/`: JavaScript propio de la app.
- `cdr22/static/img/`: imagenes usadas por la app.
- `cdr22/management/commands/`: comandos personalizados de Django.
- `theme/`: app relacionada con Tailwind.
- `theme/static_src/src/`: archivos fuente de Tailwind.
- `theme/static/css/dist/`: CSS compilado de Tailwind.
- `tests_e2e/`: pruebas E2E historicas con Playwright. Mantenerlas si existen, pero no basar trabajo nuevo en ellas sin confirmacion.

## Donde tocar segun el tipo de cambio

- Cambios en datos o reglas del dominio: revisar `cdr22/models.py`.
- Cambios en pantallas HTML: revisar `cdr22/views.py`, `cdr22/urls.py` y `cdr22/templates/`.
- Cambios visuales: revisar primero templates y luego identificar si el cambio pertenece al pipeline global de Tailwind o a CSS propio de la app.
- Estilos globales, tokens de tema, colores Tailwind y clases reutilizables con `@apply`: editar `theme/static_src/src/styles.css`.
- Estilos del layout autenticado, header, navegacion y tablas compartidas: editar `theme/static_src/src/auth.css`, que se importa desde `styles.css`.
- CSS propio de la app que no pertenezca al pipeline global de Tailwind: usar `cdr22/static/css/`.
- No editar manualmente `theme/static/css/dist/`; es salida compilada de Tailwind.
- Cambios de API: revisar `cdr22/api_views.py`, `cdr22/api_urls.py` y `cdr22/serializers.py`.
- Nuevos comandos administrativos: crear archivos en `cdr22/management/commands/`.
- Configuracion global: revisar `config/settings.py`.
- Rutas globales: revisar `config/urls.py`.

## Flujo de desarrollo local

En Windows, desde la raiz del proyecto:

```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py tailwind start
```

En otra terminal:

```powershell
.\venv\Scripts\activate
python manage.py runserver
```

Para compilar Tailwind para produccion:

```powershell
python manage.py tailwind build
```

## Migraciones y base de datos

- Si se cambian modelos en `cdr22/models.py`, revisar si corresponde crear migraciones.
- No modificar ni borrar `db.sqlite3` salvo peticion explicita.
- No asumir datos de produccion a partir de la base local.

## Variables de entorno

- Usar `.env.example` como referencia.
- No mostrar, copiar ni modificar secretos de `.env` sin autorizacion explicita.

## Pruebas

- Antes de cambios importantes, revisar si hay pruebas existentes aplicables.
- Playwright existe en `tests_e2e/`, pero esta deprecado para trabajo nuevo del proyecto.
- Si se agregan pruebas nuevas, preferir pruebas Django/pytest normales salvo que el usuario pida E2E.

## Reglas para agentes

- Leer la estructura existente antes de editar.
- Mantener los cambios acotados a la tarea.
- No hacer refactors no solicitados.
- Para endpoints `POST`, `PUT`, `PATCH` y `DELETE`, seguir el patrón de serializers + services + respuestas JSON estándar descrito en `docs/api-pattern.md`.
- Para estilos del dashboard, reutilizar las clases semánticas descritas en `docs/styles-pattern.md` antes de repetir utilities largas de Tailwind.
- No tocar `venv/`, `__pycache__/`, `.pytest_cache/`, screenshots generados o archivos compilados si no es necesario.
- No agregar nuevas dependencias sin justificarlo y confirmarlo.
- Seguir el estilo actual de templates, vistas y rutas.
- Si una tarea menciona configuracion, primero revisar `config/settings.py` y despues la app afectada.
- Si una tarea menciona frontend, primero identificar si el cambio pertenece a templates, CSS estatico de `cdr22`, `theme/static_src/src/styles.css` o `theme/static_src/src/auth.css`.
