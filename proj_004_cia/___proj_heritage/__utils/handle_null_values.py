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


if __name__ == "__main__":
    """Test null value handling utilities."""

    print("=" * 70)
    print("NULL VALUE HANDLING UTILITIES TEST")
    print("=" * 70)

    # Test 1: Normalize empty
    print("\n1. NORMALIZE EMPTY VALUES")
    print("-" * 70)

    normalize_tests = [
        ("", "Empty string"),
        ("null", "String 'null'"),
        ("NULL", "String 'NULL'"),
        ("actual value", "Real value"),
        (None, "None"),
        ("0", "Zero string"),
    ]

    for value, description in normalize_tests:
        result = normalize_empty(value)
        print(f"{description:20} Input: {repr(value):20} → Output: {repr(result)}")

    # Test 2: Handle null with defaults
    print("\n2. HANDLE NULL WITH DEFAULTS")
    print("-" * 70)

    handle_tests = [
        (None, "Not available", "area_hectares", "Null with default"),
        (150, "Not available", "area_hectares", "Valid value"),
        ("", "Unknown", "name", "Empty string"),
    ]

    for value, default, field, description in handle_tests:
        result = handle_null(value, default, field)
        print(f"{description:25} Value: {repr(value):15} Default: {repr(default):20} → {repr(result)}")

    # Test 3: Has value check
    print("\n3. HAS VALUE CHECK")
    print("-" * 70)

    has_value_tests = [
        (None, False, "None"),
        ("", False, "Empty string"),
        (0, True, "Zero (valid)"),
        ([], False, "Empty list"),
        ({}, False, "Empty dict"),
        ("text", True, "Valid string"),
        ([1, 2], True, "Valid list"),
    ]

    for value, expected, description in has_value_tests:
        result = has_value(value)
        status = "✓" if result == expected else "✗"
        print(f"{status} {description:20} Value: {repr(value):15} Has value: {result}")

    # Test 4: Safe get from dict
    print("\n4. SAFE GET FROM DICTIONARY")
    print("-" * 70)

    test_dict = {
        "name": "Butrint",
        "area": None,
        "description": ""
    }

    safe_get_tests = [
        ("name", "Unknown", "Existing key"),
        ("area", "Unknown", "Null value"),
        ("description", "No description", "Empty string"),
        ("missing", "Default", "Missing key"),
    ]

    for key, default, description in safe_get_tests:
        result = safe_get(test_dict, key, default)
        print(f"{description:20} Key: {key:15} Default: {default:20} → {repr(result)}")

    # Test 5: Handle missing coordinates
    print("\n5. HANDLE MISSING COORDINATES")
    print("-" * 70)

    coords_tests = [
        ({'lat': 39.7, 'lon': 20.0}, "Valid coordinates"),
        (None, "None value"),
        ({'lat': None, 'lon': None}, "Null coordinates"),
        ({}, "Empty dict"),
    ]

    for coords, description in coords_tests:
        result = handle_missing_coordinates(coords, "Test Site")
        print(f"\n{description}:")
        print(f"  Input:     {coords}")
        print(f"  Available: {result['available']}")
        if result['available']:
            print(f"  Lat/Lon:   {result['latitude']}, {result['longitude']}")
        else:
            print(f"  Note:      {result.get('note')}")

    # Test 6: Handle missing area
    print("\n6. HANDLE MISSING AREA")
    print("-" * 70)

    area_tests = [
        (150.0, "Valid area"),
        (None, "Missing area"),
        (0.0, "Zero area (edge case)"),
    ]

    for area, description in area_tests:
        result = handle_missing_area(area)
        print(f"\n{description}: Input={area}")
        if result['available']:
            print(f"  Hectares:  {result['hectares']}")
            print(f"  Sq km:     {result['square_km']}")
            print(f"  Sq miles:  {result['square_miles']}")
        else:
            print(f"  Note:      {result.get('note')}")

    # Test 7: Handle missing image
    print("\n7. HANDLE MISSING IMAGE")
    print("-" * 70)

    image_tests = [
        ({'url': 'https://example.com/image.jpg', 'width': 800, 'height': 600}, None, "Valid main image"),
        (None, "https://gallery.com/img1.jpg,https://gallery.com/img2.jpg", "Gallery fallback"),
        (None, None, "No images available"),
    ]

    for main_img, gallery, description in image_tests:
        result = handle_missing_image(main_img, gallery)
        print(f"\n{description}:")
        print(f"  Available: {result['available']}")
        if result['available']:
            print(f"  URL:       {result['url']}")
            print(f"  Source:    {result.get('source')}")
        else:
            print(f"  Note:      {result.get('note')}")

    # Summary
    print("\n" + "=" * 70)
    print("✓ All null value handling tests completed!")
    print("=" * 70)
