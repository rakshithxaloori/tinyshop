from app.lib.error import TinyshopException, StatusCodeEnum, ErrorTypeEnum


def bool_sanitizer(value: str, name: str, optional: bool = False) -> None:
    """Check if the bool_str is a valid bool and return a bool."""
    if value is None and optional:
        return None
    if value not in ["true", "false"]:
        raise TinyshopException(
            status_code=StatusCodeEnum.BAD_REQUEST,
            error_type=ErrorTypeEnum.INVALID_REQUEST_ERROR,
            param=name,
            message=f"'{value}' is an invalid '{name}' value. Expected 'true' or 'false'.",
        )

    return value == "true"


def urls_sanitizer(urls: set[str], name: str, count_max: int | None = None) -> set[str]:
    if count_max and len(urls) > count_max:
        raise TinyshopException(
            status_code=StatusCodeEnum.BAD_REQUEST,
            error_type=ErrorTypeEnum.INVALID_REQUEST_ERROR,
            param=name,
            message=f"'{name}' has {len(urls)} urls. Expected at most {count_max}",
        )
    s_urls: set[str] = set()
    # Throw error for empty strings too
    return urls
