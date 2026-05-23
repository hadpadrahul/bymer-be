# Bymer Dynamic Website Backend

## What This Is

This project is a lightweight Django and Django REST Framework backend for one real company website with a dynamic landing-page style frontend. The frontend will consume stable APIs for admin-managed content such as banners, global company details, products, machinery, people, credibility assets, FAQs, and form submissions.

This is not a CMS, page builder, no-code platform, or generic content engine. Django Admin is the primary CRUD interface, and the API should stay practical, predictable, fast, and easy for the frontend to consume.

## Core Value

The backend lets non-technical admins manage website content safely while giving the frontend stable, fast APIs that do not need backend changes for normal content edits.

## Requirements

### Validated

(None yet - ship to validate)

### Active

- [ ] Provide a production-ready Django + DRF project configured for local SQLite and production PostgreSQL.
- [ ] Make Django Admin the central content-management interface for all dynamic website data.
- [ ] Support admin-managed global website content, including company details, contact details, logos, social links, banners, shared statistics, and footer/header data.
- [ ] Support page-specific content through a stable page-centric API where whole-page assembly is useful.
- [ ] Support repeatable content collections that can grow, shrink, be ordered, and be hidden without code changes.
- [ ] Support catalog data for product categories, products, machinery, and plant-specific machinery filtering.
- [ ] Support credibility content including team members, history/timeline, client partners, testimonials/documents, certifications, awards, and FAQs.
- [ ] Store contact inquiries and career applications through validated write-only public endpoints, with submissions visible in admin.
- [ ] Keep API response shapes stable, lean, ordered, filterable, and frontend-friendly.
- [ ] Keep the schema practical: normalized relational models by default, JSONField only when it clearly reduces complexity.
- [ ] Optimize read-heavy endpoints with sensible queryset selection and no unnecessary nesting or overfetching.
- [ ] Prepare production deployment with environment-based settings, Docker, static/media handling, and Nginx reverse proxy assumptions.
- [ ] Document the API contract, model purpose, admin usage, and deployment expectations.

### Out of Scope

- A generic CMS or page builder - this project serves one website and should not become a platform.
- Public user accounts - admin/staff authentication is enough for internal content management.
- A new endpoint for every small content variation - prefer stable page and collection endpoints.
- Forcing every static paragraph into admin - truly fixed marketing copy can remain frontend-owned when that keeps the backend simpler.
- Real-time features, chat, ecommerce checkout, or complex workflow automation - not needed for the stated site.
- Third-party dependencies without clear value - keep the backend small and maintainable.

## Context

The known website pages are Home, About Us, Our Team, Our History, Automotive Products, Non-Automotive Products, Machinery for Plant I and Plant II, Process, Testimonials, Quality Assurance, Contact Us, and Career With Us.

Dynamic content should include product grids and product details, machinery listings, team members, history/timeline items, testimonial and document assets, banners, global contact details, social links, statistics, FAQs, certifications, awards, and form submissions.

The backend should use a hybrid API style:

- Page-centric API for routes that benefit from whole-page rendering, such as `GET /api/pages/<slug>/`.
- Collection APIs for reusable data and grids, such as company profile, social links, statistics, FAQs, timeline entries, team members, testimonials, product categories, products, machinery, contact form, and career form.

The implementation should stay friendly to a dynamic frontend: arrays should be ordered, optional content should be safe to omit, media URLs should be explicit, and the frontend should not assume fixed item counts.

## Constraints

- **Tech stack**: Django, Django REST Framework, PostgreSQL in production, SQLite acceptable locally - matches the intended backend and deployment model.
- **Content strategy**: Admin-managed only when content changes, repeats, grows, or needs CRUD - prevents overengineering.
- **API design**: Stable page and collection endpoints with filtering, ordering, and pagination where useful - avoids one-off endpoint sprawl.
- **Data modeling**: Prefer relational models; use JSONField only for genuinely flexible section-specific data - keeps queries and admin usable.
- **Performance**: Read-heavy website APIs should use lean serializers, `select_related`, `prefetch_related`, and no unnecessary deep nesting.
- **Deployment**: Use `.env` settings, Docker, Gunicorn, Whitenoise/static handling, and Nginx for reverse proxy plus static/media serving.
- **Branching**: `main` stays clean for application code only; `development` carries GSD planning artifacts. Agent/runtime directories such as `.codex/`, `.cursor/`, `.gemini/`, `.claude/`, and `.agent/` are ignored.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use Django + DRF | Best fit for admin-first content management with a clean REST API. | Pending |
| Use Django Admin as the content UI | Internal editors need practical CRUD, not a custom admin product. | Pending |
| Use hybrid page-centric and collection APIs | Whole-page payloads help dynamic pages while collection endpoints keep reusable data simple. | Pending |
| Keep public authentication out of scope | The project does not require public user accounts. | Pending |
| Keep `main` clean and develop on `development` | Supports GSD planning without polluting the app-only release branch. | Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition**:
1. Requirements invalidated? Move to Out of Scope with reason.
2. Requirements validated? Move to Validated with phase reference.
3. New requirements emerged? Add to Active.
4. Decisions to log? Add to Key Decisions.
5. "What This Is" still accurate? Update if drifted.

**After each milestone**:
1. Full review of all sections.
2. Core Value check - still the right priority?
3. Audit Out of Scope - reasons still valid?
4. Update Context with current state.

---
*Last updated: 2026-05-23 after initialization*
