# Plan 05-02 Summary — Globals, pages, catalog, content CRUD

**Status:** Complete

## Delivered

- Content registry (`dashboard/registry.py`) driving list/create/edit URLs for 13 collections
- ModelForms with shared Tailwind styling (`dashboard/forms.py`, `FORM_MAP`)
- Template CRUD: list (search, active filter, pagination), create/edit forms, deactivate/remove
- Company profile singleton at `/dashboard/globals/profile/`
- Website pages list/detail/edit with code-mapped section links (`pages/page_compose.py`)
- `/api/admin/<registry_key>/<pk>/toggle-active/` and `.../order/` PATCH endpoints
- `{% copy_api_url %}` template tag for public API path copy buttons
- Audit logging on registry and page writes
- Tests in `dashboard/tests/test_crud.py`

## Notes

- Page sections remain read-only in the dashboard (by design); editors manage underlying collections
- Category delete blocked when products exist (deactivate path shows error message)
