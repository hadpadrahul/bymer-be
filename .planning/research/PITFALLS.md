# Pitfalls Research

## Overbuilding a CMS

**Risk:** Page sections become arbitrary, nested, and hard to validate.

**Warning signs:**
- Generic block models appear before concrete page needs.
- Admin users must understand schema concepts instead of editing content.
- API responses expose backend implementation details.

**Prevention:**
- Start with explicit models for known dynamic content.
- Add flexible section data only where a page genuinely needs it.
- Keep the page endpoint as assembly, not a page builder engine.

## Underbuilding the Admin

**Risk:** Data exists, but editors cannot manage it comfortably.

**Warning signs:**
- No search/filter fields on content-heavy admin pages.
- Ordering requires raw numeric edits without useful list display.
- Media-heavy models have no preview or helpful grouping.

**Prevention:**
- Treat admin classes as product surface.
- Add ordering, list display, search, filters, fieldsets, and previews where they save editor effort.

## API Drift

**Risk:** The frontend depends on unstable response shapes or one-off endpoints.

**Warning signs:**
- New endpoint for every frontend tweak.
- Serializers expose too many raw model fields.
- Optional content is returned inconsistently.

**Prevention:**
- Document sample responses early.
- Use stable serializers with explicit frontend fields.
- Prefer filters and optional fields over endpoint multiplication.

## Query Explosion

**Risk:** Page rendering becomes slow as content grows.

**Warning signs:**
- Page endpoint loops through related objects without prefetching.
- Serializer methods perform database queries.
- Admin-created content volume increases and endpoint latency rises.

**Prevention:**
- Use `select_related` and `prefetch_related` in view/query layers.
- Keep serializer methods pure or precomputed.
- Add tests or debug checks around query counts for page endpoints.

## Media Handling Assumptions

**Risk:** Local media works but production uploads/static files break.

**Warning signs:**
- Hardcoded media URLs.
- No clear volume mount or backup plan.
- Docker/Nginx setup ignores uploaded files.

**Prevention:**
- Define `MEDIA_ROOT`, `MEDIA_URL`, static collection, and Nginx serving assumptions early.
- Keep uploads under predictable paths.
- Include media backup notes in deployment docs.

## Form Spam and Validation Gaps

**Risk:** Public form endpoints collect poor data or spam.

**Warning signs:**
- Missing length/email/phone validation.
- Form endpoints return stored submissions publicly.
- No source page or timestamp context.

**Prevention:**
- Make form endpoints write-only.
- Validate fields explicitly.
- Store source page and timestamps.
- Defer anti-spam integrations until needed, but leave room for them.
