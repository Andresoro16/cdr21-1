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

## Comandos

### Agregar Stock

```bash
python manage.py add_stock --sku "PROD-001" --cantidad 50
python manage.py add_stock --id 5 --cantidad 30
```
