# DRF Backend Source of Truth — Dynamic Website Project

## 1) Project Summary

Build a lightweight Django + Django REST Framework backend for a single real website project with a dynamic landing-page style frontend. This is **not** a CMS, page builder, or no-code platform. The backend should be practical, production-friendly, easy to maintain, fast to query, and simple for the frontend to consume.

The frontend will render most content dynamically from APIs. Django Admin will be the primary content-management interface. The system must be flexible enough that content can grow, shrink, be reordered, or change structure over time without needing new APIs for every small change.

## 2) Core Goals

- Keep the backend small, clean, and efficient.
- Make Django Admin the central CRUD interface for content.
- Support dynamic pages, banners, repeatable blocks, media, and form submissions.
- Avoid redesigning the backend every time content changes.
- Keep frontend integration simple and predictable.
- Keep performance strong for a mostly read-heavy website.
- Allow future additions in fields, field types, and content volume with minimal code changes.

## 3) Important Constraints

- Do not overengineer.
- Do not turn this into a generic CMS.
- Do not build unnecessary abstractions.
- Do not create one API per tiny content change.
- Do not hardcode content that clearly belongs in admin.
- Do not introduce unnecessary third-party dependencies.

## 4) Project Assumptions

### Content behavior
- Content may change in quantity and shape over time.
- Repeatable collections may gain or lose items freely.
- Some sections may later need extra fields, extra buttons, or more media.
- Some pages may use the same layout with different data.
- Some page copy may remain hardcoded on the frontend if it is truly static and not worth managing in admin.

### Deployment and environment
- Local development may use SQLite.
- Production should use PostgreSQL.
- Media files may be stored in `media/` on the VPS and served by Nginx.
- Docker is expected for deployment.
- Nginx should sit in front of the app for static/media serving and reverse proxying.
- Admin authentication is enough for internal content management; no public user accounts are required for this project.

## 5) Content Strategy

Use a practical structure with three content layers:

### A. Global content
Content repeated across the site:
- company details
- contact details
- logos
- social links
- global banners
- shared statistics
- footer/header content

### B. Page-specific content
Content tied to a page route:
- hero/banner content
- page metadata
- page sections
- section ordering
- section-specific media
- optional CTA blocks

### C. Repeatable collections
Structured reusable content that may grow/shrink:
- team members
- timeline items
- client logos
- testimonials/documents
- FAQs
- products
- machinery
- certifications
- awards

## 6) Site Structure

The known pages are:

- Home
- About Us
- Our Team
- Our History
- Automotive Products
- Non-Automotive Products
- Machinery (Plant I & Plant II)
- Process
- Testimonials
- Quality Assurance
- Contact Us
- Career With Us

### Static vs dynamic split
Some pages contain mostly static editorial text and can stay hardcoded on the frontend if that is simpler and truly unlikely to change. Examples include process-style explanatory paragraphs, mission/vision-style copy, and other long-form marketing text that is not meant to be edited frequently.

The following should be dynamic and admin-managed:
- product grids and product details
- machinery listings
- team members
- history/timeline items
- testimonial/document assets
- banners
- global contact details
- social links
- statistics
- FAQs
- certifications and awards
- form submissions

## 7) Recommended Model Strategy

The data model should stay small but flexible. Use normalized relational models where structure matters, and use JSONField only where flexibility is clearly useful.

### Global / shared models
- `CompanyProfile` — singleton for brand and contact details
- `SocialLink` — platform, URL, order, active flag
- `SiteMediaBanner` — page/route, title, media file, optional video URL, active flag
- `CompanyStatistic` — label, value, order, active flag

### Content / credibility models
- `TimelineEvent` — year, title, description, order, active flag
- `TeamMember` — photo, full name, designation, bio, management pillar flag, order
- `ClientPartner` — client logo/name, order, active flag
- `TestimonialDocument` — image/PDF, client or supplier name, type, order, active flag
- `Certification` — title, image/PDF, order, active flag
- `Award` — title, image/PDF, order, active flag
- `FAQ` — question, answer, order, active flag

### Catalog models
- `ProductCategory` — name, slug, order, active flag
- `Product` — category, name, slug, image, description, customer, specification, optional extra details, order, active flag
- `MachineryPlant` or a plant field on machinery — enough to separate Plant I and Plant II
- `Machinery` — plant, name, image, total machines, make, year of purchase, tonnage/capacity, platen size/dimensions, order, active flag

### Form models
- `ContactInquiry` — name, email, phone, subject, message, source page, created at
- `JobApplication` — name, dob, address, city, contact, email, qualifications, experience, area of interest, expected CTC, preferred contact date/time, optional resume file if later approved

### Optional future-friendly models
Only add if needed later:
- SEO metadata model linked to page slug
- Page model if the frontend needs a formal route registry
- PageSection model if the site needs full section composition from admin
- Document download model if PDFs need broader reuse

## 8) Architectural Decision: Page-Centric + Collection APIs

Use a hybrid approach.

### Page-centric APIs
Useful for whole-page rendering and hero/section assembly:
- `GET /api/pages/<slug>/`

A page endpoint should return:
- page title
- optional SEO metadata
- banner/hero data
- section list
- ordered content needed for that page
- any page-specific CTA or helper data

### Collection APIs
Useful for reusable data grids, filters, and repeatable content:
- `GET /api/globals/company-profile/`
- `GET /api/globals/social-links/`
- `GET /api/globals/statistics/`
- `GET /api/content/faqs/`
- `GET /api/content/timelines/`
- `GET /api/content/team/?pillar=true`
- `GET /api/content/testimonials/?type=customer`
- `GET /api/catalog/categories/`
- `GET /api/catalog/products/?category=<slug>`
- `GET /api/catalog/machinery/?plant=<value>`
- `POST /api/forms/contact/`
- `POST /api/forms/career/`

### Rule
Do not create new endpoints for every tiny content variation. Prefer stable endpoints with filtering, ordering, and optional fields.

## 9) API Design Rules

- Return only what the frontend needs.
- Keep response shapes stable.
- Use ordering consistently.
- Use filtering for list endpoints.
- Keep serializers lean.
- Avoid deeply nested payloads unless a page endpoint genuinely needs them.
- Use pagination for larger or future-growing collections.
- Keep write endpoints simple and validated.
- Prefer one predictable structure over many one-off responses.

## 10) Frontend Integration Rules

The frontend should be able to:
- fetch a page by slug
- render sections by `type`
- use ordered data directly
- render repeatable collections as arrays
- ignore optional sections when absent
- use image URLs and related metadata from the API
- avoid hardcoded assumptions about content counts
- avoid needing backend changes for normal content edits

### Static frontend content
Some fixed marketing paragraphs or purely editorial text can be hardcoded in the frontend if they are intentionally static and rarely change. Do not force every piece of text into admin if it makes the backend heavier without benefit.

## 11) Django Admin Requirements

Django Admin must be easy for non-technical content editing.

### Admin should support:
- CRUD for all required content models
- simple labels and good field grouping
- ordering fields for repeatable content
- image/file previews where helpful
- active/published toggles
- search and filter support
- inline editing only where it improves usability
- easy edits for repeated content blocks

### Admin-first rule
If content may change over time, it should be manageable from admin unless there is a strong reason not to.

## 12) Performance Expectations

This backend is read-heavy and should stay fast.

### Performance rules
- minimize DB queries
- use `select_related` and `prefetch_related` where useful
- keep serializer logic light
- avoid overfetching
- avoid huge unnecessary nested responses
- keep endpoint count reasonable
- make caching possible later if needed
- do not add complexity that does not improve speed or maintainability

### Production reality
Even though the website is small, the content system must stay robust because admins may add more content, fields, and assets later.

## 13) Validation and Flexibility

The backend should be flexible enough to absorb future content changes.

### Design for:
- extra fields later
- field type changes later
- more items in collections later
- optional image/file additions later
- optional button/link additions later
- optional page-level metadata later

### Validation principle
Keep validation strict enough to protect data quality, but not so rigid that future changes become painful.

## 14) Forms and Submission Handling

### Contact / quote form
Store submissions in the database and expose a simple POST endpoint. Optionally send notifications by email later.

### Career form
Store the submission and validate carefully. If the client later confirms it, add a `resume_file` field. For now, keep the form model ready for that extension.

### Recommendation
Form endpoints should be write-only from the frontend perspective, but submissions should remain visible in admin for review.

## 15) SEO and Metadata

SEO metadata was not fully available from the old site. Treat it as a future-friendly enhancement.

### Recommended approach
- keep page-level metadata support ready
- allow page title, meta description, OG image, canonical URL if needed later
- if not required immediately, keep the fields optional

## 16) Deployment and Environment

### Local development
- SQLite is acceptable for local development.

### Production
- PostgreSQL should be used in production.
- Docker should be used for deployment.
- Nginx should serve media/static files and reverse proxy requests.
- `.env`-based settings should be used for environment-specific configuration.

### Media
- Use `media/` on the VPS for uploaded files if that is the chosen deployment approach.
- Make backups part of deployment planning.

## 17) Implementation Order

1. Confirm final page list and dynamic content scope.
2. Finalize global models and shared content models.
3. Finalize catalog models for products and machinery.
4. Finalize form models and validation.
5. Build serializers and endpoints.
6. Build Django Admin carefully.
7. Add query optimization and cleanup.
8. Add docs and API examples.
9. Add production settings and Docker deployment files.
10. Validate with frontend integration.

## 18) Documentation Deliverables

Maintain a single source-of-truth markdown file that includes:
- project understanding
- architecture decisions
- model list
- relationships
- endpoint list
- frontend contract
- admin structure
- performance notes
- deployment notes
- implementation order
- constraints and flexibility rules

## 19) Final Working Rule

If content is repeated, changes often, or may expand later, make it dynamic and admin-managed.
If content is truly fixed and would only add unnecessary complexity, keep it static on the frontend.
The system should stay simple, fast, and user-friendly while remaining easy to extend later.
