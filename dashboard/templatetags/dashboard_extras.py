from django import template

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
