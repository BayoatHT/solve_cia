"""
Parse components: multi-location site details.
"""

import re
from typing import Dict, List


def parse_components(site: Dict) -> Dict:
    """
    Parse component data for multi-location sites.

    Args:
        site: Raw site dictionary

    Returns:
        Dictionary with component count and location details

    Example:
        >>> site = {
        ...     "components_count": 2,
        ...     "components_list": "{name: See, ref: 1363-061, latitude: 47.8, longitude: 13.4}, ..."
        ... }
        >>> parse_components(site)
        {
            'count': 2,
            'locations': [...]
        }
    """
    components_count = site.get('components_count', 0)
    components_str = site.get('components_list', '')

    # Parse components list
    locations = parse_components_string(components_str)

    return {
        'count': components_count,
        'locations': locations
    }


def parse_components_string(components_str: str) -> List[Dict]:
    """
    Parse components string to list of location dictionaries.

    Args:
        components_str: Component string from raw data

    Returns:
        List of component dictionaries

    Example:
        >>> parse_components_string("{name: See, ref: 1363-061, latitude: 47.8, longitude: 13.4}")
        [{'name': 'See', 'ref': '1363-061', 'latitude': 47.8, 'longitude': 13.4}]
    """
    if not components_str:
        return []

    # Clean up string
    components_str = components_str.strip()
    if not components_str.startswith('{'):
        return []

    # Split by component boundaries: }, {
    component_parts = re.split(r'\}\s*,?\s*\{', components_str)

    components = []
    for part in component_parts:
        # Remove leading/trailing braces
        part = part.strip('{}').strip()

        # Parse key-value pairs
        component = {}

        # Pattern: key: value (handles values with spaces)
        for match in re.finditer(r'(\w+):\s*([^,}]+?)(?=,\s*\w+:|$)', part):
            key = match.group(1).strip()
            value = match.group(2).strip()

            # Type conversion
            if key in ['latitude', 'longitude']:
                try:
                    component[key] = float(value)
                except (ValueError, TypeError):
                    component[key] = None
            else:
                component[key] = value

        if component and 'name' in component:
            components.append(component)

    return components
