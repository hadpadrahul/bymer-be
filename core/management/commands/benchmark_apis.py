import json
import statistics
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from urllib.parse import urlparse

from django.core.management.base import BaseCommand


@dataclass
class CheckResult:
    name: str
    method: str
    path: str
    status: int | None = None
    elapsed_ms: float | None = None
    bytes_read: int = 0
    detail: str = ""
    ok: bool = False
    item_count: int | None = None


class Command(BaseCommand):
    help = "Benchmark public APIs against a running server and log latency/media details."

    def add_arguments(self, parser):
        parser.add_argument(
            "--base-url",
            default="http://127.0.0.1:8000",
            help="Base URL of a running Django server (default: http://127.0.0.1:8000).",
        )
        parser.add_argument(
            "--skip-media",
            action="store_true",
            help="Do not fetch image/file URLs found in API responses.",
        )
        parser.add_argument(
            "--skip-write",
            action="store_true",
            help="Skip POST form endpoint checks.",
        )
        parser.add_argument(
            "--rounds",
            type=int,
            default=1,
            help="Repeat GET checks N times and report median latency (default: 1).",
        )

    def handle(self, *args, **options):
        base_url = options["base_url"].rstrip("/")
        rounds = max(1, options["rounds"])

        self.stdout.write(self.style.MIGRATE_HEADING(f"API benchmark @ {base_url}"))
        self.stdout.write(f"  Rounds: {rounds}")
        self.stdout.write("")

        health, _ = self._fetch("GET", f"{base_url}/api/health/", "Health check")
        if not health.ok:
            self.stdout.write(
                self.style.ERROR(
                    "Server not reachable. Start it with: python manage.py runserver"
                )
            )
            self._print_summary([health], [])
            return

        checks = [
            ("GET", "/api/globals/company-profile/", "Globals: company profile"),
            ("GET", "/api/globals/social-links/", "Globals: social links"),
            ("GET", "/api/globals/statistics/", "Globals: statistics"),
            ("GET", "/api/globals/banners/", "Globals: banners"),
            ("GET", "/api/content/team/", "Content: team"),
            ("GET", "/api/content/team/?pillar=true", "Content: team (pillar=true)"),
            ("GET", "/api/content/timelines/", "Content: timelines"),
            ("GET", "/api/content/clients/", "Content: clients"),
            ("GET", "/api/content/testimonials/", "Content: testimonials"),
            ("GET", "/api/content/testimonials/?type=customer", "Content: testimonials (customer)"),
            ("GET", "/api/content/certifications/", "Content: certifications"),
            ("GET", "/api/content/awards/", "Content: awards"),
            ("GET", "/api/content/faqs/", "Content: faqs"),
            ("GET", "/api/catalog/categories/", "Catalog: categories"),
            ("GET", "/api/catalog/products/", "Catalog: products"),
            ("GET", "/api/catalog/products/?category=automotive-products", "Catalog: products (automotive)"),
            ("GET", "/api/catalog/machinery/", "Catalog: machinery"),
            ("GET", "/api/catalog/machinery/?plant=plant_1", "Catalog: machinery (plant_1)"),
            ("GET", "/api/pages/home/", "Page: home"),
            ("GET", "/api/pages/our-team/", "Page: our-team"),
            ("GET", "/api/pages/our-history/", "Page: our-history"),
            ("GET", "/api/pages/testimonials/", "Page: testimonials"),
            ("GET", "/api/pages/quality-assurance/", "Page: quality-assurance"),
            ("GET", "/api/pages/automotive-products/", "Page: automotive-products"),
            ("GET", "/api/pages/non-automotive-products/", "Page: non-automotive-products"),
            ("GET", "/api/pages/machinery/", "Page: machinery"),
            ("GET", "/api/pages/contact-us/", "Page: contact-us"),
            ("GET", "/api/pages/inactive-demo-page/", "Page: inactive (expect 404)"),
            ("GET", "/api/schema/", "OpenAPI schema"),
        ]

        bodies: dict[str, object] = {}
        results: list[CheckResult] = [health]

        for method, path, name in checks:
            url = f"{base_url}{path}"
            timings: list[float] = []
            last_result: CheckResult | None = None
            last_body: object | None = None

            for _ in range(rounds):
                last_result, last_body = self._fetch(method, url, name, base_url=base_url)
                if last_result.elapsed_ms is not None:
                    timings.append(last_result.elapsed_ms)

            if last_result is None:
                continue
            if rounds > 1 and timings:
                last_result.elapsed_ms = statistics.median(timings)
                last_result.detail = f"median of {rounds} runs ({min(timings):.1f}–{max(timings):.1f} ms)"
            if last_body is not None:
                bodies[name] = last_body
            results.append(last_result)

        media_results: list[CheckResult] = []
        if not options["skip_media"]:
            media_urls = sorted(self._collect_media_urls(bodies))
            self.stdout.write("")
            self.stdout.write(self.style.MIGRATE_HEADING(f"Media URL checks ({len(media_urls)} files)"))
            for index, url in enumerate(media_urls, start=1):
                fetch_url = url if url.startswith("http") else f"{base_url}{url}"
                display = urlparse(url).path if url.startswith("http") else url
                media_results.append(self._fetch_media(fetch_url, index, display))

        if not options["skip_write"]:
            self.stdout.write("")
            self.stdout.write(self.style.MIGRATE_HEADING("Write endpoints"))
            contact_payload = json.dumps(
                {
                    "name": "Benchmark User",
                    "email": "benchmark@demo.bymer.local",
                    "phone": "7777777777",
                    "subject": "Benchmark",
                    "message": "API benchmark contact submission.",
                    "source_page": "contact-us",
                }
            ).encode("utf-8")
            results.append(
                self._fetch_post(
                    f"{base_url}/api/forms/contact/",
                    "POST /api/forms/contact/",
                    contact_payload,
                    base_url=base_url,
                )
            )
            career_payload = json.dumps(
                {
                    "full_name": "Benchmark Applicant",
                    "address": "Benchmark Street",
                    "contact_number": "6666666666",
                    "email": "benchmark-career@demo.bymer.local",
                    "qualifications": "B.E. Mechanical",
                }
            ).encode("utf-8")
            results.append(
                self._fetch_post(
                    f"{base_url}/api/forms/career/",
                    "POST /api/forms/career/",
                    career_payload,
                    base_url=base_url,
                )
            )
            get_forms, _ = self._fetch(
                "GET",
                f"{base_url}/api/forms/contact/",
                "Forms: GET contact (expect 405)",
                base_url=base_url,
            )
            get_forms.ok = get_forms.status == 405
            results.append(get_forms)

        self._print_detail_table(results)
        if media_results:
            self._print_media_table(media_results)
        self._print_insights(results, bodies, media_results)
        self._print_summary(results, media_results)

    def _fetch(
        self,
        method: str,
        url: str,
        name: str,
        *,
        base_url: str = "",
    ) -> tuple[CheckResult, object | None]:
        path = url.replace(base_url, "") if base_url else urlparse(url).path
        result = CheckResult(name=name, method=method, path=path or url)
        expect_404 = name == "Page: inactive (expect 404)"
        expect_405 = "expect 405" in name
        start = time.perf_counter()
        try:
            request = urllib.request.Request(url, method=method)
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read()
                result.status = response.status
                result.bytes_read = len(raw)
                result.elapsed_ms = (time.perf_counter() - start) * 1000
                body = None
                content_type = response.headers.get("Content-Type", "")
                if "json" in content_type:
                    body = json.loads(raw.decode("utf-8")) if raw else None
                    result.item_count = self._count_items(body)
                    if result.item_count is not None:
                        result.detail = f"{result.item_count} items"
                elif "yaml" in content_type or url.endswith("/schema/"):
                    result.detail = "OpenAPI document"
                if expect_404:
                    result.ok = response.status == 404
                elif expect_405:
                    result.ok = response.status == 405
                else:
                    result.ok = 200 <= response.status < 300
                return result, body
        except urllib.error.HTTPError as error:
            result.status = error.code
            result.elapsed_ms = (time.perf_counter() - start) * 1000
            result.detail = (error.read().decode("utf-8", errors="replace") or error.reason)[:120]
            if expect_404:
                result.ok = error.code == 404
            elif expect_405:
                result.ok = error.code == 405
            return result, None
        except urllib.error.URLError as error:
            result.detail = str(error.reason)
            result.elapsed_ms = (time.perf_counter() - start) * 1000
            return result, None

    def _fetch_post(self, url: str, name: str, payload: bytes, *, base_url: str) -> CheckResult:
        result = CheckResult(name=name, method="POST", path=url.replace(base_url, ""))
        start = time.perf_counter()
        try:
            request = urllib.request.Request(
                url,
                data=payload,
                method="POST",
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read()
                result.status = response.status
                result.bytes_read = len(raw)
                result.elapsed_ms = (time.perf_counter() - start) * 1000
                result.ok = response.status == 201
                return result
        except urllib.error.HTTPError as error:
            result.status = error.code
            result.elapsed_ms = (time.perf_counter() - start) * 1000
            result.detail = error.read().decode("utf-8", errors="replace")[:200]
            return result
        except urllib.error.URLError as error:
            result.detail = str(error.reason)
            result.elapsed_ms = (time.perf_counter() - start) * 1000
            return result

    def _fetch_media(self, url: str, index: int, display_path: str) -> CheckResult:
        result = CheckResult(name=f"Media #{index}", method="GET", path=display_path)
        start = time.perf_counter()
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                raw = response.read()
                result.status = response.status
                result.bytes_read = len(raw)
                result.elapsed_ms = (time.perf_counter() - start) * 1000
                result.ok = response.status == 200 and len(raw) > 0
                result.detail = response.headers.get("Content-Type", "")
                return result
        except urllib.error.HTTPError as error:
            result.status = error.code
            result.elapsed_ms = (time.perf_counter() - start) * 1000
            result.detail = error.reason
            return result
        except urllib.error.URLError as error:
            result.detail = str(error.reason)
            result.elapsed_ms = (time.perf_counter() - start) * 1000
            return result

    def _count_items(self, body: object | None) -> int | None:
        if isinstance(body, dict):
            if "count" in body:
                return int(body["count"])
            if "results" in body and isinstance(body["results"], list):
                return len(body["results"])
            if "sections" in body and isinstance(body["sections"], list):
                return len(body["sections"])
        if isinstance(body, list):
            return len(body)
        return None

    def _collect_media_urls(self, bodies: dict[str, object]) -> set[str]:
        urls: set[str] = set()

        def walk(node):
            if isinstance(node, dict):
                for key, value in node.items():
                    if key.endswith("_url") and isinstance(value, str) and value:
                        urls.add(value)
                    else:
                        walk(value)
            elif isinstance(node, list):
                for item in node:
                    walk(item)

        for body in bodies.values():
            walk(body)
        return urls

    def _print_detail_table(self, results: list[CheckResult]):
        self.stdout.write(self.style.MIGRATE_HEADING("Endpoint results"))
        header = f"{'Status':<8} {'ms':>8} {'Bytes':>10}  {'Check'}"
        self.stdout.write(header)
        self.stdout.write("-" * len(header))
        for result in results:
            status = result.status if result.status is not None else "ERR"
            elapsed = f"{result.elapsed_ms:8.1f}" if result.elapsed_ms is not None else "     n/a"
            size = f"{result.bytes_read:10d}"
            flag = "OK" if result.ok else "FAIL"
            extra = ""
            if result.item_count is not None:
                extra = f" ({result.item_count} items)"
            if result.detail and result.detail not in (f"{result.item_count} items",):
                extra = f" — {result.detail}" if not extra else f"{extra}, {result.detail}"
            line = f"{status!s:<8} {elapsed} {size}  {result.name}{extra} [{flag}]"
            if result.ok:
                self.stdout.write(self.style.SUCCESS(line))
            else:
                self.stdout.write(self.style.ERROR(line))

    def _print_media_table(self, results: list[CheckResult]):
        header = f"{'Status':<8} {'ms':>8} {'Bytes':>10}  {'Media path'}"
        self.stdout.write(header)
        self.stdout.write("-" * len(header))
        for result in results:
            status = result.status if result.status is not None else "ERR"
            elapsed = f"{result.elapsed_ms:8.1f}" if result.elapsed_ms is not None else "     n/a"
            size = f"{result.bytes_read:10d}"
            flag = "OK" if result.ok else "FAIL"
            line = f"{status!s:<8} {elapsed} {size}  {result.path} [{flag}] {result.detail}"
            if result.ok:
                self.stdout.write(self.style.SUCCESS(line))
            else:
                self.stdout.write(self.style.ERROR(line))

    def _print_insights(
        self,
        results: list[CheckResult],
        bodies: dict[str, object],
        media_results: list[CheckResult],
    ):
        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING("Quick insights"))

        ok_reads = [
            result
            for result in results
            if result.ok and result.elapsed_ms is not None and result.method == "GET"
        ]
        if ok_reads:
            timings = [result.elapsed_ms for result in ok_reads if result.elapsed_ms is not None]
            self.stdout.write(
                f"  GET latency — min {min(timings):.1f}ms | median {statistics.median(timings):.1f}ms | max {max(timings):.1f}ms"
            )
            slowest = sorted(ok_reads, key=lambda item: item.elapsed_ms or 0, reverse=True)[:5]
            self.stdout.write("  Slowest GET endpoints:")
            for item in slowest:
                self.stdout.write(
                    f"    - {item.name}: {item.elapsed_ms:.1f}ms ({item.bytes_read} bytes)"
                )

        profile = bodies.get("Globals: company profile")
        if isinstance(profile, dict) and profile.get("logo_url"):
            self.stdout.write(f"  Company logo URL: {profile['logo_url']}")

        page_body = bodies.get("Page: home")
        if isinstance(page_body, dict):
            sections = page_body.get("sections", [])
            self.stdout.write(
                f"  Page home — {len(sections)} sections: {[section.get('type') for section in sections]}"
            )

        media_urls = self._collect_media_urls(bodies)
        self.stdout.write(f"  Unique media URLs in responses: {len(media_urls)}")
        if media_results:
            media_timings = [item.elapsed_ms for item in media_results if item.elapsed_ms]
            media_bytes = [item.bytes_read for item in media_results if item.ok]
            if media_timings:
                self.stdout.write(
                    f"  Media fetch — median {statistics.median(media_timings):.1f}ms | max {max(media_timings):.1f}ms"
                )
            if media_bytes:
                total_kb = sum(media_bytes) / 1024
                self.stdout.write(f"  Media payload total: {total_kb:.1f} KB across {len(media_bytes)} files")

        failures = [result for result in results if not result.ok]
        media_failures = [result for result in media_results if not result.ok]
        if failures or media_failures:
            self.stdout.write(
                self.style.WARNING(
                    f"  Needs attention: {len(failures)} endpoint(s), {len(media_failures)} media file(s)"
                )
            )
            for item in failures + media_failures:
                self.stdout.write(f"    - {item.name or item.path} (status={item.status})")
        else:
            self.stdout.write(self.style.SUCCESS("  All benchmark checks passed."))

    def _print_summary(self, results: list[CheckResult], media_results: list[CheckResult]):
        total = len(results)
        passed = sum(1 for result in results if result.ok)
        media_passed = sum(1 for result in media_results if result.ok)
        self.stdout.write("")
        self.stdout.write(
            self.style.MIGRATE_HEADING(
                f"Summary: {passed}/{total} checks passed"
                + (
                    f", {media_passed}/{len(media_results)} media files OK"
                    if media_results
                    else ""
                )
            )
        )
