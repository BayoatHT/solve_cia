######################################################################################################################
# CORE IMPORTS
# C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\c_00_transform_utils\parse_coordinates.py
# ---------------------------------------------------------------------------------------------------------------------
import re
from proj_004_cia.__logger.logger import app_logger
from typing import Dict, Any, List, Optional, Union, Tuple

######################################################################################################################
# NEW UTILITY: COORDINATE PARSING
######################################################################################################################


def parse_coordinates(coord_text: str) -> dict:
    """
    Parse geographic coordinates from various formats.

    Args:
        coord_text: Text containing coordinates

    Returns:
        Dictionary with latitude and longitude

    Examples:
        >>> parse_coordinates("41 54 N, 12 27 E")
        {"latitude": 41.9, "longitude": 12.45}
    """
    if not isinstance(coord_text, str) or not coord_text.strip():
        return {}

    try:
        text = coord_text.strip()

        # Pattern for degrees, minutes format: "41 54 N, 12 27 E"
        pattern = r'(\d+)\s+(\d+)\s*([NS]),?\s*(\d+)\s+(\d+)\s*([EW])'
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            lat_deg, lat_min, lat_dir, lon_deg, lon_min, lon_dir = match.groups()

            latitude = float(lat_deg) + float(lat_min) / 60
            if lat_dir.upper() == 'S':
                latitude = -latitude

            longitude = float(lon_deg) + float(lon_min) / 60
            if lon_dir.upper() == 'W':
                longitude = -longitude

            return {"latitude": latitude, "longitude": longitude}

        # Pattern for decimal degrees: "41.9, 12.45"
        decimal_pattern = r'([-+]?\d+\.?\d*),\s*([-+]?\d+\.?\d*)'
        decimal_match = re.search(decimal_pattern, text)

        if decimal_match:
            latitude = float(decimal_match.group(1))
            longitude = float(decimal_match.group(2))
            return {"latitude": latitude, "longitude": longitude}

        return {}

    except Exception as e:
        if app_logger:
            app_logger.error(f"Error parsing coordinates '{coord_text}': {e}")
        return {}
