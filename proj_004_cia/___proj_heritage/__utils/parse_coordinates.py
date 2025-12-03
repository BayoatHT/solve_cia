"""
Coordinate parsing and validation utilities.

Handles geographic coordinate extraction, validation, and formatting.
"""

from typing import Optional, Dict, Tuple


def parse_coordinates(coords_data: Optional[Dict]) -> Optional[Dict[str, Optional[float]]]:
    """
    Parse coordinate data from raw site data.

    Args:
        coords_data: Dictionary with 'lat' and 'lon' keys

    Returns:
        Dictionary with latitude and longitude, or None if invalid

    Example:
        >>> parse_coordinates({"lat": 39.745732, "lon": 20.02095})
        {'latitude': 39.745732, 'longitude': 20.02095}

        >>> parse_coordinates(None)
        None
    """
    if not coords_data:
        return None

    lat = coords_data.get('lat')
    lon = coords_data.get('lon')

    # Return None if both are missing
    if lat is None and lon is None:
        return None

    return {
        'latitude': lat,
        'longitude': lon
    }


def validate_coordinates(lat: Optional[float], lon: Optional[float]) -> bool:
    """
    Validate latitude and longitude values.

    Args:
        lat: Latitude value
        lon: Longitude value

    Returns:
        True if both coordinates are valid, False otherwise

    Rules:
        - Latitude: -90 to +90
        - Longitude: -180 to +180

    Example:
        >>> validate_coordinates(39.745732, 20.02095)
        True

        >>> validate_coordinates(100, 20)  # Invalid latitude
        False
    """
    if lat is None or lon is None:
        return False

    try:
        lat = float(lat)
        lon = float(lon)

        # Check ranges
        if not (-90 <= lat <= 90):
            return False

        if not (-180 <= lon <= 180):
            return False

        return True

    except (ValueError, TypeError):
        return False


def format_coordinates(lat: float, lon: float, precision: int = 6) -> Dict[str, str]:
    """
    Format coordinates for display.

    Args:
        lat: Latitude
        lon: Longitude
        precision: Decimal places (default: 6)

    Returns:
        Dictionary with formatted coordinates

    Example:
        >>> format_coordinates(39.745732, 20.02095)
        {
            'latitude': '39.745732',
            'longitude': '20.020950',
            'display': '39.7457°N, 20.0210°E',
            'dms': "39°44'44.6\"N, 20°01'15.4\"E"
        }
    """
    # Determine N/S, E/W
    lat_dir = 'N' if lat >= 0 else 'S'
    lon_dir = 'E' if lon >= 0 else 'W'

    lat_abs = abs(lat)
    lon_abs = abs(lon)

    # Decimal format
    lat_str = f"{lat:.{precision}f}"
    lon_str = f"{lon:.{precision}f}"

    # Display format
    display = f"{lat_abs:.4f}°{lat_dir}, {lon_abs:.4f}°{lon_dir}"

    # DMS (Degrees, Minutes, Seconds) format
    lat_dms = decimal_to_dms(lat_abs)
    lon_dms = decimal_to_dms(lon_abs)
    dms = f"{lat_dms}{lat_dir}, {lon_dms}{lon_dir}"

    return {
        'latitude': lat_str,
        'longitude': lon_str,
        'display': display,
        'dms': dms
    }


def decimal_to_dms(decimal: float) -> str:
    """
    Convert decimal degrees to DMS format.

    Args:
        decimal: Decimal degrees

    Returns:
        DMS string (e.g., "39°44'44.6\"")

    Example:
        >>> decimal_to_dms(39.745732)
        '39°44\'44.6"'
    """
    degrees = int(decimal)
    minutes_decimal = (decimal - degrees) * 60
    minutes = int(minutes_decimal)
    seconds = (minutes_decimal - minutes) * 60

    return f'{degrees}°{minutes}\'{seconds:.1f}"'


def get_coordinate_bounds(coords_list: list) -> Optional[Dict]:
    """
    Calculate bounding box for list of coordinates.

    Args:
        coords_list: List of coordinate dictionaries

    Returns:
        Dictionary with min/max lat/lon

    Example:
        >>> coords = [
        ...     {'latitude': 39.0, 'longitude': 20.0},
        ...     {'latitude': 40.0, 'longitude': 21.0}
        ... ]
        >>> get_coordinate_bounds(coords)
        {'min_lat': 39.0, 'max_lat': 40.0, 'min_lon': 20.0, 'max_lon': 21.0}
    """
    if not coords_list:
        return None

    valid_coords = [
        c for c in coords_list
        if c and c.get('latitude') is not None and c.get('longitude') is not None
    ]

    if not valid_coords:
        return None

    lats = [c['latitude'] for c in valid_coords]
    lons = [c['longitude'] for c in valid_coords]

    return {
        'min_lat': min(lats),
        'max_lat': max(lats),
        'min_lon': min(lons),
        'max_lon': max(lons),
        'center_lat': sum(lats) / len(lats),
        'center_lon': sum(lons) / len(lons),
    }


if __name__ == "__main__":
    """Test coordinate parsing utilities with real UNESCO site examples."""

    print("=" * 70)
    print("COORDINATE PARSING UTILITIES TEST")
    print("=" * 70)

    # Test 1: Parse coordinates
    print("\n1. PARSE COORDINATES")
    print("-" * 70)

    test_coords = [
        ({"lat": 39.745732, "lon": 20.02095}, "Butrint, Albania"),
        ({"lat": 13.412468, "lon": 103.866986}, "Angkor, Cambodia"),
        ({"lat": -13.163068, "lon": -72.544963}, "Machu Picchu, Peru"),
        ({"lat": 30.328542, "lon": 35.443249}, "Petra, Jordan"),
        (None, "Missing coordinates"),
        ({}, "Empty dict"),
        ({"lat": None, "lon": None}, "Null values"),
    ]

    for coords, description in test_coords:
        result = parse_coordinates(coords)
        print(f"Site: {description}")
        print(f"  Input:  {coords}")
        print(f"  Output: {result}")
        print()

    # Test 2: Validate coordinates
    print("\n2. VALIDATE COORDINATES")
    print("-" * 70)

    validation_tests = [
        (39.745732, 20.02095, True, "Valid European coordinates"),
        (13.412468, 103.866986, True, "Valid Asian coordinates"),
        (-13.163068, -72.544963, True, "Valid South American (negative)"),
        (100, 20, False, "Invalid latitude (>90)"),
        (45, 200, False, "Invalid longitude (>180)"),
        (-95, 50, False, "Invalid latitude (<-90)"),
        (0, 0, True, "Null Island (valid but unusual)"),
        (None, None, False, "None values"),
        ("invalid", "text", False, "String values"),
    ]

    for lat, lon, expected, description in validation_tests:
        valid = validate_coordinates(lat, lon)
        status = "✓" if valid == expected else "✗"
        print(f"{status} {description:40} Lat: {lat:10} Lon: {lon:10} Valid: {valid}")

    # Test 3: Format coordinates
    print("\n3. FORMAT COORDINATES")
    print("-" * 70)

    format_tests = [
        (39.745732, 20.02095, "Butrint, Albania"),
        (13.412468, 103.866986, "Angkor, Cambodia"),
        (-13.163068, -72.544963, "Machu Picchu, Peru"),
        (37.9715, 23.7257, "Acropolis, Greece"),
    ]

    for lat, lon, description in format_tests:
        formatted = format_coordinates(lat, lon)
        print(f"Site: {description}")
        print(f"  Decimal: Lat {formatted['latitude']}, Lon {formatted['longitude']}")
        print(f"  Display: {formatted['display']}")
        print(f"  DMS:     {formatted['dms']}")
        print()

    # Test 4: Decimal to DMS conversion
    print("\n4. DECIMAL TO DMS CONVERSION")
    print("-" * 70)

    dms_tests = [
        (39.745732, "39°44'44.6\""),
        (13.412468, "13°24'44.9\""),
        (0.0, "0°0'0.0\""),
        (90.0, "90°0'0.0\""),
        (45.5, "45°30'0.0\""),
    ]

    for decimal, expected_format in dms_tests:
        dms = decimal_to_dms(decimal)
        print(f"{decimal:10.6f}° → {dms:20} (Expected: {expected_format})")

    # Test 5: Get coordinate bounds
    print("\n5. GET COORDINATE BOUNDS")
    print("-" * 70)

    # Simulate multiple heritage sites in Europe
    europe_sites = [
        {'latitude': 39.745732, 'longitude': 20.02095, 'name': 'Butrint'},
        {'latitude': 41.9028, 'longitude': 12.4964, 'name': 'Rome'},
        {'latitude': 37.9715, 'longitude': 23.7257, 'name': 'Athens'},
        {'latitude': 48.8566, 'longitude': 2.3522, 'name': 'Paris'},
        {'latitude': 50.0755, 'longitude': 14.4378, 'name': 'Prague'},
    ]

    bounds = get_coordinate_bounds(europe_sites)

    if bounds:
        print("European UNESCO Sites Bounding Box:")
        print(f"  Min Latitude:  {bounds['min_lat']:.6f}° (Southernmost)")
        print(f"  Max Latitude:  {bounds['max_lat']:.6f}° (Northernmost)")
        print(f"  Min Longitude: {bounds['min_lon']:.6f}° (Westernmost)")
        print(f"  Max Longitude: {bounds['max_lon']:.6f}° (Easternmost)")
        print(f"  Center Point:  {bounds['center_lat']:.6f}°, {bounds['center_lon']:.6f}°")
        print()

        # Calculate approximate dimensions
        lat_range = bounds['max_lat'] - bounds['min_lat']
        lon_range = bounds['max_lon'] - bounds['min_lon']
        print(f"  Latitude Range:  {lat_range:.2f}°")
        print(f"  Longitude Range: {lon_range:.2f}°")
    print()

    # Test 6: Edge cases
    print("\n6. EDGE CASES")
    print("-" * 70)

    edge_cases = [
        ([], "Empty list"),
        ([{'latitude': None, 'longitude': None}], "All None values"),
        ([{'latitude': 45.0}], "Missing longitude"),
        ([{'longitude': 90.0}], "Missing latitude"),
    ]

    for coords_list, description in edge_cases:
        bounds = get_coordinate_bounds(coords_list)
        print(f"{description:30} → Bounds: {bounds}")

    # Summary
    print("\n" + "=" * 70)
    print("✓ All coordinate parsing tests completed!")
    print("=" * 70)
