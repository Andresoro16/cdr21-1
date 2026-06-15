# Patrón de estilos

Usar Tailwind como base, pero preferir clases semánticas para patrones repetidos del dashboard.

## Archivo principal

Las clases compartidas viven en:

```text
theme/static_src/src/styles.css
```

No editar manualmente el CSS compilado en `theme/static/css/dist/`.

## Convención

Para pantallas nuevas del dashboard, usar estas clases antes de repetir utilities largas:

- `dashboard-container`: contenedor principal de página.
- `dashboard-card`, `dashboard-card-header`, `dashboard-card-body`: tarjetas y secciones.
- `page-title`, `page-description`, `detail-title`, `section-title`, `section-description`: jerarquía de texto.
- `data-table-wrapper`, `data-table-wrapper-tall`, `data-table`, `data-table-head`, `data-table-row`: tablas.
- `empty-state-cell`, `empty-state`, `empty-state-icon`, `empty-state-title`, `empty-state-description`: estados vacíos.
- `status-badge`, con variantes `status-badge-success`, `status-badge-warning`, `status-badge-danger`, `status-badge-muted`.
- `btn`, con tamaños `btn-sm`, `btn-md` y variantes `btn-primary`, `btn-success`, `btn-danger`, `btn-warning`, `btn-secondary`.
- `menu-panel`, `menu-item`: menús desplegables simples.

## Regla práctica

Si una combinación de clases Tailwind se repite en varias pantallas, crear o reutilizar una clase semántica en `styles.css`.

Después de modificar estilos compartidos, verificar:

```powershell
.\venv\Scripts\python.exe manage.py tailwind build
```
