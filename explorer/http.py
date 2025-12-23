def get_csp_header_value(object_store_host: str):
    """
    Creates the value for the Content-Security-Policy HTTP header.
    The host of the object storage is needed because it needs to
    be included in some of the directives.

    :param object_store_host: host of the object storage
    :type object_store_host: str
    """
    directives = [
        "default-src 'self'",
        f"img-src 'self' {object_store_host}",
        f"media-src 'self' {object_store_host}",
        "frame-src 'none'",
        "frame-ancestors 'none'",
    ]
    return '; '.join(directives)
