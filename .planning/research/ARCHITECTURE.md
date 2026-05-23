# Architecture Research

## Shape

Build a small modular Django project with domain apps instead of a single large app or an over-fragmented app tree.

Recommended app boundaries:

- `core`: shared utilities, base models, environment-aware settings helpers if needed.
- `pages`: page registry, page metadata, page banners, optional page sections.
- `globals`: company profile, social links, shared statistics, global banners or global content.
- `content`: team, timeline, clients, testimonials/documents, certifications, awards, FAQs.
- `catalog`: product categories, products, machinery, machinery plant grouping.
- `forms`: contact inquiries and career applications.
- `api`: router/schema composition if the project prefers a central API module.

## Data Flow

1. Admin creates or edits content in Django Admin.
2. Models enforce ordering, active flags, slugs, and validation.
3. Querysets filter to active/published records for public endpoints.
4. Serializers return lean frontend-facing fields, including absolute or configured media URLs when appropriate.
5. Page endpoint composes page-specific banner/metadata plus the collections required by that page.
6. Collection endpoints expose reusable lists with filtering and ordering.
7. Form endpoints validate public submissions and store them for admin review.

## API Boundaries

Page-centric:

- `GET /api/pages/<slug>/`

Collection:

- `GET /api/globals/company-profile/`
- `GET /api/globals/social-links/`
- `GET /api/globals/statistics/`
- `GET /api/content/faqs/`
- `GET /api/content/timeline/`
- `GET /api/content/team/?pillar=true`
- `GET /api/content/testimonials/?type=customer`
- `GET /api/catalog/categories/`
- `GET /api/catalog/products/?category=<slug>`
- `GET /api/catalog/machinery/?plant=<value>`
- `POST /api/forms/contact/`
- `POST /api/forms/career/`

## Model Patterns

- Common fields for repeatable content: `order`, `is_active`, `created_at`, `updated_at`.
- Slugs for routeable/filterable content such as pages, categories, products, and machinery where useful.
- Optional fields where future content variance is expected.
- `JSONField` only for bounded extras, such as product specifications or page-section configuration that would otherwise create many low-value tables.
- File/image upload paths grouped by domain.

## Build Order

1. Project/settings foundation, dependency setup, app structure, environment config.
2. Shared model/admin conventions.
3. Global and content models with admin.
4. Catalog models with admin and filtering.
5. Forms models, validation, and admin visibility.
6. Serializers, viewsets, routers, schema docs.
7. Page endpoint composition.
8. Query optimization, tests, fixtures/factories, docs.
9. Docker, production settings, static/media handling.

## Architecture Guardrail

Every abstraction must serve this one website. If a generic framework would make the admin or API harder to reason about, use explicit models and explicit serializers instead.
