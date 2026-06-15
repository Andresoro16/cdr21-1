# Patrón de API y servicios

Usar este patrón para endpoints nuevos o refactors de `POST`, `PUT`, `PATCH` y `DELETE`.

## Responsabilidades

- `api_views.py`: recibe JSON, ejecuta serializers, llama servicios y retorna respuestas JSON.
- `serializers.py`: valida datos de entrada y define errores por campo.
- `services/`: contiene reglas de negocio y escrituras en base de datos.
- `api_responses.py`: centraliza el formato de respuestas JSON.
- `views.py`: solo para pantallas HTML que renderizan templates.

## Respuesta JSON estándar

Éxito:

```json
{
  "ok": true,
  "mensaje": "Operación exitosa",
  "data": {},
  "errores": null
}
```

Error:

```json
{
  "ok": false,
  "mensaje": "Hay errores en el formulario",
  "data": null,
  "errores": {
    "campo": ["Mensaje de error"]
  }
}
```

## Regla práctica

La vista no debe contener reglas de negocio largas. Si una operación crea, actualiza, anula, aplica stock o modifica varias tablas, mover esa lógica a un servicio.
