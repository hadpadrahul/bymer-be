# Requirements: Bymer Dynamic Website Backend

**Defined:** 2026-05-23
**Core Value:** The backend lets non-technical admins manage website content safely while giving the frontend stable, fast APIs that do not need backend changes for normal content edits.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Foundation

- [x] **FOUND-01**: Developer can install and run a Django + DRF project locally using documented environment variables.
- [x] **FOUND-02**: Developer can use SQLite locally and configure PostgreSQL for production through `.env` settings.
- [x] **FOUND-03**: Developer can manage static and uploaded media through configured `STATIC_*` and `MEDIA_*` settings.
- [x] **FOUND-04**: API consumer can access all public API endpoints under a consistent `/api/` URL namespace.
- [x] **FOUND-05**: Developer can view generated OpenAPI documentation for the public API.

### Admin Content Management

- [x] **ADMIN-01**: Admin can manage dynamic website content through Django Admin without public user accounts.
- [x] **ADMIN-02**: Admin can search and filter content-heavy models from Django Admin.
- [x] **ADMIN-03**: Admin can order repeatable content through explicit order fields.
- [x] **ADMIN-04**: Admin can hide or publish applicable content through active/published flags.
- [x] **ADMIN-05**: Admin can preview or identify uploaded image/file assets where useful in admin lists or detail pages.

### Global Content

- [x] **GLOB-01**: Admin can manage a singleton company profile with brand and contact details.
- [x] **GLOB-02**: Admin can manage social links with platform, URL, ordering, and active status.
- [x] **GLOB-03**: Admin can manage shared company statistics with label, value, ordering, and active status.
- [x] **GLOB-04**: Admin can manage page or site banners with title, media, optional video URL, ordering, and active status.
- [x] **GLOB-05**: Frontend can retrieve global company profile, social links, statistics, and banners through stable API responses.

### Page Content

- [x] **PAGE-01**: Admin can manage known website pages by slug, title, optional metadata, and active status.
- [x] **PAGE-02**: Admin can associate page-specific banner or helper content with a known page.
- [x] **PAGE-03**: Frontend can fetch `GET /api/pages/<slug>/` for page-ready metadata, banner, and relevant section data.
- [x] **PAGE-04**: Frontend can safely ignore optional page fields or sections when they are absent.

### Repeatable Content

- [x] **CONT-01**: Admin can manage team members with photo, name, designation, bio, management pillar flag, ordering, and active status.
- [x] **CONT-02**: Admin can manage timeline/history entries with year, title, description, ordering, and active status.
- [x] **CONT-03**: Admin can manage client or partner entries with logo/name, ordering, and active status.
- [x] **CONT-04**: Admin can manage testimonial or document assets with client/supplier name, type, image/PDF, ordering, and active status.
- [x] **CONT-05**: Admin can manage certifications with title, image/PDF, ordering, and active status.
- [x] **CONT-06**: Admin can manage awards with title, image/PDF, ordering, and active status.
- [x] **CONT-07**: Admin can manage FAQs with question, answer, ordering, and active status.
- [x] **CONT-08**: Frontend can retrieve repeatable content collections as ordered arrays with stable field names.

### Catalog

- [x] **CAT-01**: Admin can manage product categories with name, slug, ordering, and active status.
- [x] **CAT-02**: Admin can manage products with category, name, slug, image, description, customer/specification fields, optional extra details, ordering, and active status.
- [x] **CAT-03**: Admin can manage machinery entries with plant grouping, name, image, total machines, make, purchase year, tonnage/capacity, dimensions, ordering, and active status.
- [x] **CAT-04**: Frontend can filter products by category slug.
- [x] **CAT-05**: Frontend can filter machinery by plant.
- [x] **CAT-06**: Frontend receives catalog items in deterministic order and never needs to assume a fixed item count.

### Forms

- [x] **FORM-01**: Visitor can submit a contact inquiry with name, email, phone, subject, message, source page, and timestamp.
- [x] **FORM-02**: Visitor can submit a career application with personal, contact, qualification, experience, interest, expected CTC, and preferred contact date/time fields.
- [x] **FORM-03**: Visitor receives validation errors for incomplete or invalid form submissions.
- [x] **FORM-04**: Admin can view, search, filter, and review contact inquiries in Django Admin.
- [x] **FORM-05**: Admin can view, search, filter, and review career applications in Django Admin.
- [x] **FORM-06**: Frontend cannot list or retrieve stored form submissions through public endpoints.

### API Quality

- [x] **API-01**: API list endpoints return active content by default.
- [x] **API-02**: API list endpoints support filtering where filtering is part of the frontend contract.
- [x] **API-03**: API list endpoints support pagination where content may grow.
- [x] **API-04**: API serializers return only frontend-relevant fields and avoid unnecessary nesting.
- [x] **API-05**: API responses include usable media URLs or media metadata for uploaded assets.
- [x] **API-06**: API endpoints use optimized querysets for related objects and common page reads.

### Testing, Documentation, and Deployment

- [x] **OPS-01**: Developer can run automated tests for models, serializers, and API endpoints.
- [x] **OPS-02**: Developer can generate or inspect sample API responses for frontend integration.
- [x] **OPS-03**: Developer can build and run the backend with Docker.
- [x] **OPS-04**: Operator has documented production settings for Gunicorn, Nginx, static files, media files, and environment variables.
- [x] **OPS-05**: Operator has documented media backup assumptions for VPS-hosted uploads.

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Enhancements

- **SEO-01**: Admin can manage richer SEO metadata, canonical URLs, and Open Graph fields if the frontend needs them.
- **EMAIL-01**: ~~System can send email notifications for contact and career submissions.~~ Shipped in Phase 5 (`ADMIN_NOTIFICATION_EMAILS`); keep in v2 only if richer templates/webhooks are needed later.
- **FORM-EXT-01**: Career applications can accept resume uploads when the client confirms that requirement.
- **DOC-01**: Admin can manage a broader reusable document-download library.
- **MEDIA-01**: Uploaded media can move to object storage if VPS disk storage becomes insufficient.
- **CACHE-01**: Read-heavy endpoints can add caching once production traffic justifies it.
- **SPAM-01**: Public forms can add CAPTCHA or another anti-spam layer if spam appears.

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Generic CMS or page builder | The project serves one website and should stay simple. |
| Public user accounts | Admin/staff authentication is enough for content management. |
| Ecommerce checkout | Products are informational catalog content, not a store. |
| Real-time chat or messaging | Not part of the stated website backend. |
| Workflow automation for editors | Adds complexity before a real need exists. |
| One-off endpoint per content tweak | Stable page and collection APIs are the intended contract. |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| FOUND-01 | Phase 1 | Complete |
| FOUND-02 | Phase 1 | Complete |
| FOUND-03 | Phase 1 | Complete |
| FOUND-04 | Phase 1 | Complete |
| FOUND-05 | Phase 1 | Complete |
| ADMIN-01 | Phase 2 | Complete |
| ADMIN-02 | Phase 2 | Complete |
| ADMIN-03 | Phase 2 | Complete |
| ADMIN-04 | Phase 2 | Complete |
| ADMIN-05 | Phase 2 | Complete |
| GLOB-01 | Phase 2 | Complete |
| GLOB-02 | Phase 2 | Complete |
| GLOB-03 | Phase 2 | Complete |
| GLOB-04 | Phase 2 | Complete |
| GLOB-05 | Phase 3 | Complete |
| PAGE-01 | Phase 2 | Complete |
| PAGE-02 | Phase 2 | Complete |
| PAGE-03 | Phase 3 | Complete |
| PAGE-04 | Phase 3 | Complete |
| CONT-01 | Phase 2 | Complete |
| CONT-02 | Phase 2 | Complete |
| CONT-03 | Phase 2 | Complete |
| CONT-04 | Phase 2 | Complete |
| CONT-05 | Phase 2 | Complete |
| CONT-06 | Phase 2 | Complete |
| CONT-07 | Phase 2 | Complete |
| CONT-08 | Phase 3 | Complete |
| CAT-01 | Phase 2 | Complete |
| CAT-02 | Phase 2 | Complete |
| CAT-03 | Phase 2 | Complete |
| CAT-04 | Phase 3 | Complete |
| CAT-05 | Phase 3 | Complete |
| CAT-06 | Phase 3 | Complete |
| FORM-01 | Phase 3 | Complete |
| FORM-02 | Phase 3 | Complete |
| FORM-03 | Phase 3 | Complete |
| FORM-04 | Phase 2 | Complete |
| FORM-05 | Phase 2 | Complete |
| FORM-06 | Phase 3 | Complete |
| API-01 | Phase 3 | Complete |
| API-02 | Phase 3 | Complete |
| API-03 | Phase 3 | Complete |
| API-04 | Phase 3 | Complete |
| API-05 | Phase 3 | Complete |
| API-06 | Phase 3 | Complete |
| OPS-01 | Phase 1 | Complete |
| OPS-02 | Phase 4 | Complete |
| OPS-03 | Phase 4 | Complete |
| OPS-04 | Phase 4 | Complete |
| OPS-05 | Phase 4 | Complete |

**Coverage:**
- v1 requirements: 50 total
- Mapped to phases: 50
- Unmapped: 0

---
*Requirements defined: 2026-05-23*
*Last updated: 2026-05-23 after Phase 4 completion (v1 milestone complete)*
