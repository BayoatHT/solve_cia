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
