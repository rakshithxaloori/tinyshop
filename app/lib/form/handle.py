import re
import unicodedata


def get_handle(name: str) -> str:
    # Normalize the product name to NFKD form
    handle = unicodedata.normalize("NFKD", name)
    # Convert to lowercase
    handle = handle.lower()
    # Replace spaces and special characters with hyphens
    handle = re.sub(r"\s+", "-", handle)
    # Remove non-alphanumeric characters except for hyphens
    handle = re.sub(r"[^a-z0-9-]", "", handle)
    # Remove leading and trailing hyphens
    handle = handle.strip("-")
    return handle
