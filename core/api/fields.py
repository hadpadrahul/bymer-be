def build_absolute_media_url(request, file_field):
    if not file_field:
        return None
    if request is None:
        return file_field.url
    return request.build_absolute_uri(file_field.url)
