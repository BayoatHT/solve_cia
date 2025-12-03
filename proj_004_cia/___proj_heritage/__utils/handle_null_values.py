"""
Null value handling utilities.

Provides consistent handling of null, None, and empty values.
"""

from typing import Any, Optional


def normalize_empty(value: Any) -> Optional[Any]:
    """
    Convert empty strings and string nulls to None.

    Args:
        value: Value to normalize

    Returns:
        None if value is empty/null, otherwise the value

    Example:
        >>> normalize_empty("")
        None

        >>> normalize_empty("null")
        None

        >>> normalize_empty("actual value")
        'actual value'
    """
    if value == "" or value == "null" or value == "NULL":
        return None

    return value


def handle_null(value: Any, default: Any = None, field_name: str = None) -> Any:
    """
    Handle null values with optional default and field-specific handling.

    Args:
        value: Value to check
        default: Default value if null
        field_name: Optional field name for context-specific handling

    Returns:
        Value or default

    Example:
        >>> handle_null(None, "Not available")
        'Not available'

        >>> handle_null(150, "Not available")
        150

        >>> handle_null(None, {"value": None, "note": "not_reported"}, "area_hectares")
        {'value': None, 'note': 'not_reported'}
    """
    if value is None:
        return default

    return value


def create_null_structure(field_name: str, note: str = "not_available") -> dict:
    """
    Create standardized null value structure.

    Args:
        field_name: Name of the field
        note: Note explaining why value is null

    Returns:
        Dictionary with null value and note

    Example:
        >>> create_null_structure("coordinates", "site_coordinates_unavailable")
        {
            'value': None,
            'note': 'site_coordinates_unavailable',
            'field': 'coordinates'
        }
    """
    return {
        'value': None,
        'note': note,
        'field': field_name
    }


def has_value(value: Any) -> bool:
    """
    Check if value is not null/empty.

    Args:
        value: Value to check

    Returns:
        True if value exists and is not empty

    Example:
        >>> has_value(None)
        False

        >>> has_value("")
        False

        >>> has_value(0)
        True

        >>> has_value([])
        False
    """
    if value is None:
        return False

    if isinstance(value, str) and value.strip() == "":
        return False

    if isinstance(value, (list, dict, set)) and len(value) == 0:
        return False

    return True


def safe_get(data: dict, key: str, default: Any = None) -> Any:
    """
    Safely get value from dictionary with null handling.

    Args:
        data: Dictionary to get value from
        key: Key to retrieve
        default: Default value if key missing or value is null

    Returns:
        Value or default

    Example:
        >>> safe_get({"name": "Butrint"}, "name")
        'Butrint'

        >>> safe_get({"name": None}, "name", "Unknown")
        'Unknown'

        >>> safe_get({}, "missing", "Default")
        'Default'
    """
    if key not in data:
        return default

    value = data[key]

    # Normalize empty strings
    value = normalize_empty(value)

    if value is None:
        return default

    return value


def handle_missing_coordinates(coords: Optional[dict], site_name: str = None) -> dict:
    """
    Handle missing coordinate data with standardized structure.

    Args:
        coords: Coordinate data or None
        site_name: Optional site name for logging

    Returns:
        Standardized coordinate structure

    Example:
        >>> handle_missing_coordinates(None, "Butrint")
        {
            'latitude': None,
            'longitude': None,
            'available': False,
            'note': 'coordinates_not_available'
        }

        >>> handle_missing_coordinates({'lat': 39.7, 'lon': 20.0})
        {
            'latitude': 39.7,
            'longitude': 20.0,
            'available': True
        }
    """
    if not coords or coords.get('lat') is None or coords.get('lon') is None:
        return {
            'latitude': None,
            'longitude': None,
            'available': False,
            'note': 'coordinates_not_available'
        }

    return {
        'latitude': coords['lat'],
        'longitude': coords['lon'],
        'available': True
    }


def handle_missing_area(area: Optional[float]) -> dict:
    """
    Handle missing area data.

    Args:
        area: Area in hectares or None

    Returns:
        Standardized area structure

    Example:
        >>> handle_missing_area(None)
        {'hectares': None, 'available': False, 'note': 'area_not_reported'}

        >>> handle_missing_area(150.0)
        {
            'hectares': 150.0,
            'square_km': 1.5,
            'square_miles': 0.579,
            'available': True
        }
    """
    if area is None:
        return {
            'hectares': None,
            'available': False,
            'note': 'area_not_reported'
        }

    return {
        'hectares': area,
        'square_km': round(area / 100, 2),
        'square_miles': round(area / 247.105, 3),
        'available': True
    }


def handle_missing_image(main_image: Optional[dict], gallery_urls: str = None) -> dict:
    """
    Handle missing main image with fallback to gallery.

    Args:
        main_image: Main image data or None
        gallery_urls: Comma-separated gallery URLs

    Returns:
        Standardized image structure

    Example:
        >>> handle_missing_image(None)
        {'url': None, 'available': False, 'note': 'image_not_available'}

        >>> handle_missing_image(None, "https://whc.unesco.org/image.jpg")
        {
            'url': 'https://whc.unesco.org/image.jpg',
            'available': True,
            'source': 'gallery_first'
        }
    """
    if main_image and main_image.get('url'):
        return {
            'url': main_image['url'],
            'filename': main_image.get('filename'),
            'dimensions': {
                'width': main_image.get('width'),
                'height': main_image.get('height')
            },
            'available': True,
            'source': 'main_image'
        }

    # Try gallery fallback
    if gallery_urls:
        urls = [u.strip() for u in gallery_urls.split(',')]
        if urls:
            return {
                'url': urls[0],
                'filename': None,
                'dimensions': None,
                'available': True,
                'source': 'gallery_first'
            }

    return {
        'url': None,
        'available': False,
        'note': 'image_not_available'
    }
