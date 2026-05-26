<!-- GSD:project-start source:PROJECT.md -->
## Project

**Bymer Dynamic Website Backend**

This project is a lightweight Django and Django REST Framework backend for one real company website with a dynamic landing-page style frontend. The frontend will consume stable APIs for admin-managed content such as banners, global company details, products, machinery, people, credibility assets, FAQs, and form submissions.

This is not a CMS, page builder, no-code platform, or generic content engine. Django Admin is the primary CRUD interface, and the API should stay practical, predictable, fast, and easy for the frontend to consume.

**Core Value:** The backend lets non-technical admins manage website content safely while giving the frontend stable, fast APIs that do not need backend changes for normal content edits.

### Constraints

- **Tech stack**: Django, Django REST Framework, PostgreSQL in production, SQLite acceptable locally - matches the intended backend and deployment model.
- **Content strategy**: Admin-managed only when content changes, repeats, grows, or needs CRUD - prevents overengineering.
- **API design**: Stable page and collection endpoints with filtering, ordering, and pagination where useful - avoids one-off endpoint sprawl.
- **Data modeling**: Prefer relational models; use JSONField only for genuinely flexible section-specific data - keeps queries and admin usable.
- **Performance**: Read-heavy website APIs should use lean serializers, `select_related`, `prefetch_related`, and no unnecessary deep nesting.
- **Deployment**: Use `.env` settings, Docker, Gunicorn, Whitenoise/static handling, and Nginx for reverse proxy plus static/media serving.
- **Branching**: `main` stays clean for application code only; `development` carries GSD planning artifacts. Agent/runtime directories such as `.codex/`, `.cursor/`, `.gemini/`, `.claude/`, and `.agent/` are ignored.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->
## Technology Stack

## Recommendation
## Core Runtime
- **Python**: Use a current Python version supported by Django 5.2, preferably Python 3.12 or 3.13 during setup.
- **Django**: Use Django 5.2 LTS. It is the safest default for a production site because it receives security support through April 2028.
- **Django REST Framework**: Use the current stable DRF release family. As of May 2026, DRF 3.17.1 is published; confirm compatibility in the lock file when installing.
- **Database**: SQLite locally, PostgreSQL in production.
- **Server**: Gunicorn behind Nginx.
- **Static files**: Whitenoise for app static assets, with Nginx serving collected static and uploaded media in production.
## Project Libraries
- `Django`
- `djangorestframework`
- `django-environ`
- `django-cors-headers`
- `django-filter`
- `drf-spectacular`
- `Pillow`
- `gunicorn`
- `whitenoise`
- `psycopg2-binary`
- `pytest`
- `pytest-django`
- `factory_boy`
- `Faker`
## Optional Later
- `drf-spectacular-sidecar` only if self-hosted Swagger/ReDoc assets are needed.
- Email backend/provider package only when notification emails are confirmed.
- Dedicated object storage client only if uploaded media moves away from VPS disk.
## What Not To Use
- Wagtail or a full CMS: too broad for the one-site admin-first scope.
- Django CMS/page builders: unnecessary abstraction and higher maintenance.
- Celery: not needed unless async email, media processing, or scheduled jobs become real requirements.
- GraphQL: the frontend contract is straightforward REST with page and collection endpoints.
## Confidence
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
