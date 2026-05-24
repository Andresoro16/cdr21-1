## Ejecucion del servidor en local

- Abrir una terminal dentro del proyecto
- ejecutar `.\venv\Scripts\activate`
- ejecutar `pip install -r requirements.txt`
- ejecutar ` python manage.py tailwind start`
- Abrimos otra terminal
- ejecutar `python manage.py runserver`
- Abrir en el navegador la URL que nos da el ultimo comando.

## Produccion
- python manage.py tailwind build

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
