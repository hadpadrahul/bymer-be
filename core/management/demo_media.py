from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image


def make_demo_image(filename: str, color: tuple[int, int, int]) -> ContentFile:
    image = Image.new("RGB", (640, 400), color=color)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue(), name=filename)


def load_image_from_dir(media_dir: Path, basename: str) -> ContentFile | None:
    """Return the first matching image from media_dir (jpg/jpeg/png/webp)."""
    if not media_dir.is_dir():
        return None
    for extension in (".jpg", ".jpeg", ".png", ".webp"):
        candidate = media_dir / f"{basename}{extension}"
        if candidate.is_file():
            return ContentFile(candidate.read_bytes(), name=candidate.name)
    return None
