# Feature Research

## Table Stakes

### Admin Content Management

- Admin can create, edit, order, activate/deactivate, search, and filter all dynamic content.
- Admin list pages use useful columns, filters, and search fields.
- Media fields are practical for images, PDFs, and future optional uploads.

### Global Website Content

- Company profile and contact details.
- Logos and brand media where needed.
- Social links.
- Shared statistics.
- Global banners or page banners.
- Footer/header data if the frontend needs it dynamically.

### Page Content

- Stable page endpoint by slug.
- Optional page title, SEO fields, banner/hero, sections, CTA fields, and helper data.
- Frontend can ignore absent optional sections.

### Repeatable Collections

- Team members.
- Timeline/history items.
- Client partners/logos.
- Testimonials or document assets.
- Certifications.
- Awards.
- FAQs.

### Catalog

- Product categories.
- Products with category, slug, image, description, customer/specification fields, optional extra details, order, and active flag.
- Machinery with plant grouping, machine details, capacity/tonnage, dimensions, order, and active flag.
- Filtering by category, plant, type, active status, and other useful query params.

### Forms

- Contact inquiry POST endpoint.
- Career application POST endpoint.
- Form submissions stored in DB and visible in admin.
- Resume upload deferred until explicitly approved, but model/API should be easy to extend.

### API Quality

- Stable response shapes.
- Ordered list responses.
- Pagination for future-growing collections.
- Filtering through `django-filter`.
- Schema documentation through `drf-spectacular`.

## Differentiators

- A page endpoint that assembles just enough page data to simplify the frontend without becoming a page builder.
- Admin previews and well-grouped fieldsets for media-heavy models.
- Clear sample responses for frontend integration.
- Query-conscious serializers and viewsets from the first implementation phase.

## Anti-Features

- Generic page builder UI.
- Arbitrary nested page composition.
- Public accounts, user profiles, carts, payments, or ecommerce checkout.
- Workflow-heavy admin customizations before real editor pain exists.
- New custom endpoints for every content tweak.

## Complexity Notes

- Low to medium: global content, social links, FAQs, statistics, banners.
- Medium: product and machinery catalog because filtering, slugs, media, and ordering must stay consistent.
- Medium: page endpoint because it must balance convenience with scope control.
- Medium: forms because validation and spam considerations need care, even if the endpoint is simple.
