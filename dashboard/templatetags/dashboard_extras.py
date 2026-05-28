from django import template

from dashboard.registry import nav_groups

register = template.Library()


@register.filter
def get_attr(obj, name):
    value = getattr(obj, name, "")
    if callable(value) and not isinstance(value, type):
        try:
            value = value()
        except TypeError:
            pass
    if value is True:
        return "Yes"
    if value is False:
        return "No"
    return value


@register.simple_tag(takes_context=True)
def copy_button(context, url_path, label="Copy API URL"):
    request = context.get("request")
    if request:
        full = request.build_absolute_uri(url_path)
    else:
        full = url_path
    return {
        "url": full,
        "path": url_path,
        "label": label,
    }


@register.inclusion_tag("dashboard/partials/copy_api.html", takes_context=True)
def copy_api_url(context, path):
    request = context.get("request")
    absolute = request.build_absolute_uri(path) if request else path
    return {"absolute_url": absolute, "path": path}


@register.simple_tag
def dashboard_nav_groups():
    groups = nav_groups()
    ordered = []
    for group_name in ("Globals", "Content", "Catalog"):
        entries = groups.get(group_name, [])
        if entries:
            ordered.append((group_name, entries))
    for group_name, entries in groups.items():
        if group_name not in {"Globals", "Content", "Catalog"}:
            ordered.append((group_name, entries))
    return ordered


@register.filter
def is_image_field(field):
    widget_name = getattr(getattr(field, "field", None), "widget", None)
    input_type = getattr(widget_name, "input_type", "")
    return input_type == "file" and hasattr(field.value(), "url")


@register.filter
def file_url(field):
    value = field.value()
    if not value:
        return ""
    try:
        return value.url
    except Exception:
        return ""
