def join_prefix(*parts: str) -> str:
    """
    Safely join URL prefixes like Flask blueprints or API namespaces.
    Ensures a single leading slash, no double slashes.

    Usage:

    >>> join_prefix("/api", "v1")
    '/api/v1'
    >>> join_prefix("/api/", "/v1/")
    '/api/v1'
    >>> join_prefix("", "/users")
    '/users'
    >>> join_prefix("/api", None, "users")
    '/api/users'
    >>> join_prefix("/root/", "/path/", "/to/", "resource")
    '/root/path/to/resource'
    >>> join_prefix("no-slash", "in-front")
    'no-slash/in-front'
    """
    return "/" + "/".join(
        x for x in (p.strip("/") for p in parts if p)
        if x
    )
