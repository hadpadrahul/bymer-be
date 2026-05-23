# Requirements: Bymer Dynamic Website Backend

**Defined:** 2026-05-23
**Core Value:** The backend lets non-technical admins manage website content safely while giving the frontend stable, fast APIs that do not need backend changes for normal content edits.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Foundation

- [ ] **FOUND-01**: Developer can install and run a Django + DRF project locally using documented environment variables.
- [ ] **FOUND-02**: Developer can use SQLite locally and configure PostgreSQL for production through `.env` settings.
- [ ] **FOUND-03**: Developer can manage static and uploaded media through configured `STATIC_*` and `MEDIA_*` settings.
- [ ] **FOUND-04**: API consumer can access all public API endpoints under a consistent `/api/` URL namespace.
- [ ] **FOUND-05**: Developer can view generated OpenAPI documentation for the public API.

### Admin Content Management

- [ ] **ADMIN-01**: Admin can manage dynamic website content through Django Admin without public user accounts.
- [ ] **ADMIN-02**: Admin can search and filter content-heavy models from Django Admin.
- [ ] **ADMIN-03**: Admin can order repeatable content through explicit order fields.
- [ ] **ADMIN-04**: Admin can hide or publish applicable content through active/published flags.
- [ ] **ADMIN-05**: Admin can preview or identify uploaded image/file assets where useful in admin lists or detail pages.

### Global Content

- [ ] **GLOB-01**: Admin can manage a singleton company profile with brand and contact details.
- [ ] **GLOB-02**: Admin can manage social links with platform, URL, ordering, and active status.
- [ ] **GLOB-03**: Admin can manage shared company statistics with label, value, ordering, and active status.
- [ ] **GLOB-04**: Admin can manage page or site banners with title, media, optional video URL, ordering, and active status.
- [ ] **GLOB-05**: Frontend can retrieve global company profile, social links, statistics, and banners through stable API responses.

### Page Content

- [ ] **PAGE-01**: Admin can manage known website pages by slug, title, optional metadata, and active status.
- [ ] **PAGE-02**: Admin can associate page-specific banner or helper content with a known page.
- [ ] **PAGE-03**: Frontend can fetch `GET /api/pages/<slug>/` for page-ready metadata, banner, and relevant section data.
- [ ] **PAGE-04**: Frontend can safely ignore optional page fields or sections when they are absent.

### Repeatable Content

- [ ] **CONT-01**: Admin can manage team members with photo, name, designation, bio, management pillar flag, ordering, and active status.
- [ ] **CONT-02**: Admin can manage timeline/history entries with year, title, description, ordering, and active status.
- [ ] **CONT-03**: Admin can manage client or partner entries with logo/name, ordering, and active status.
- [ ] **CONT-04**: Admin can manage testimonial or document assets with client/supplier name, type, image/PDF, ordering, and active status.
- [ ] **CONT-05**: Admin can manage certifications with title, image/PDF, ordering, and active status.
- [ ] **CONT-06**: Admin can manage awards with title, image/PDF, ordering, and active status.
- [ ] **CONT-07**: Admin can manage FAQs with question, answer, ordering, and active status.
- [ ] **CONT-08**: Frontend can retrieve repeatable content collections as ordered arrays with stable field names.

### Catalog

- [ ] **CAT-01**: Admin can manage product categories with name, slug, ordering, and active status.
- [ ] **CAT-02**: Admin can manage products with category, name, slug, image, description, customer/specification fields, optional extra details, ordering, and active status.
- [ ] **CAT-03**: Admin can manage machinery entries with plant grouping, name, image, total machines, make, purchase year, tonnage/capacity, dimensions, ordering, and active status.
- [ ] **CAT-04**: Frontend can filter products by category slug.
- [ ] **CAT-05**: Frontend can filter machinery by plant.
- [ ] **CAT-06**: Frontend receives catalog items in deterministic order and never needs to assume a fixed item count.

### Forms

- [ ] **FORM-01**: Visitor can submit a contact inquiry with name, email, phone, subject, message, source page, and timestamp.
- [ ] **FORM-02**: Visitor can submit a career application with personal, contact, qualification, experience, interest, expected CTC, and preferred contact date/time fields.
- [ ] **FORM-03**: Visitor receives validation errors for incomplete or invalid form submissions.
- [ ] **FORM-04**: Admin can view, search, filter, and review contact inquiries in Django Admin.
- [ ] **FORM-05**: Admin can view, search, filter, and review career applications in Django Admin.
- [ ] **FORM-06**: Frontend cannot list or retrieve stored form submissions through public endpoints.

### API Quality

- [ ] **API-01**: API list endpoints return active content by default.
- [ ] **API-02**: API list endpoints support filtering where filtering is part of the frontend contract.
- [ ] **API-03**: API list endpoints support pagination where content may grow.
- [ ] **API-04**: API serializers return only frontend-relevant fields and avoid unnecessary nesting.
- [ ] **API-05**: API responses include usable media URLs or media metadata for uploaded assets.
- [ ] **API-06**: API endpoints use optimized querysets for related objects and common page reads.

### Testing, Documentation, and Deployment

- [ ] **OPS-01**: Developer can run automated tests for models, serializers, and API endpoints.
- [ ] **OPS-02**: Developer can generate or inspect sample API responses for frontend integration.
- [ ] **OPS-03**: Developer can build and run the backend with Docker.
- [ ] **OPS-04**: Operator has documented production settings for Gunicorn, Nginx, static files, media files, and environment variables.
- [ ] **OPS-05**: Operator has documented media backup assumptions for VPS-hosted uploads.

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Enhancements

- **SEO-01**: Admin can manage richer SEO metadata, canonical URLs, and Open Graph fields if the frontend needs them.
- **EMAIL-01**: System can send email notifications for contact and career submissions.
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
| FOUND-01 | Phase 1 | Pending |
| FOUND-02 | Phase 1 | Pending |
| FOUND-03 | Phase 1 | Pending |
| FOUND-04 | Phase 1 | Pending |
| FOUND-05 | Phase 1 | Pending |
| ADMIN-01 | Phase 2 | Pending |
| ADMIN-02 | Phase 2 | Pending |
| ADMIN-03 | Phase 2 | Pending |
| ADMIN-04 | Phase 2 | Pending |
| ADMIN-05 | Phase 2 | Pending |
| GLOB-01 | Phase 2 | Pending |
| GLOB-02 | Phase 2 | Pending |
| GLOB-03 | Phase 2 | Pending |
| GLOB-04 | Phase 2 | Pending |
| GLOB-05 | Phase 3 | Pending |
| PAGE-01 | Phase 2 | Pending |
| PAGE-02 | Phase 2 | Pending |
| PAGE-03 | Phase 3 | Pending |
| PAGE-04 | Phase 3 | Pending |
| CONT-01 | Phase 2 | Pending |
| CONT-02 | Phase 2 | Pending |
| CONT-03 | Phase 2 | Pending |
| CONT-04 | Phase 2 | Pending |
| CONT-05 | Phase 2 | Pending |
| CONT-06 | Phase 2 | Pending |
| CONT-07 | Phase 2 | Pending |
| CONT-08 | Phase 3 | Pending |
| CAT-01 | Phase 2 | Pending |
| CAT-02 | Phase 2 | Pending |
| CAT-03 | Phase 2 | Pending |
| CAT-04 | Phase 3 | Pending |
| CAT-05 | Phase 3 | Pending |
| CAT-06 | Phase 3 | Pending |
| FORM-01 | Phase 3 | Pending |
| FORM-02 | Phase 3 | Pending |
| FORM-03 | Phase 3 | Pending |
| FORM-04 | Phase 2 | Pending |
| FORM-05 | Phase 2 | Pending |
| FORM-06 | Phase 3 | Pending |
| API-01 | Phase 3 | Pending |
| API-02 | Phase 3 | Pending |
| API-03 | Phase 3 | Pending |
| API-04 | Phase 3 | Pending |
| API-05 | Phase 3 | Pending |
| API-06 | Phase 3 | Pending |
| OPS-01 | Phase 1 | Pending |
| OPS-02 | Phase 4 | Pending |
| OPS-03 | Phase 4 | Pending |
| OPS-04 | Phase 4 | Pending |
| OPS-05 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 50 total
- Mapped to phases: 50
- Unmapped: 0

---
*Requirements defined: 2026-05-23*
*Last updated: 2026-05-23 after roadmap creation*
