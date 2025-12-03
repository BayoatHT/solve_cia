"""
Parse classification attributes: category, criteria, area.
"""

from typing import Dict
from proj_004_cia.___proj_heritage.__utils.parse_criteria import parse_criteria
from proj_004_cia.___proj_heritage.__utils.handle_null_values import handle_missing_area


def parse_classification(site: Dict) -> Dict:
    """
    Parse all classification attributes from raw site data.

    Args:
        site: Raw site dictionary

    Returns:
        Dictionary with category, criteria, and area data

    Example:
        >>> site = {
        ...     "category": "Cultural",
        ...     "category_id": 1,
        ...     "cultural_criteria": "c1, c2, c3",
        ...     "natural_criteria": None,
        ...     "criteria_txt": "(i)(ii)(iii)",
        ...     "area_hectares": 150.0
        ... }
        >>> parse_classification(site)
        {
            'category': {...},
            'criteria': {...},
            'area': {...}
        }
    """
    # Parse category
    category = {
        'name': site.get('category'),
        'id': site.get('category_id')
    }

    # Parse criteria
    criteria = parse_criteria(
        cultural_criteria=site.get('cultural_criteria'),
        natural_criteria=site.get('natural_criteria'),
        criteria_txt=site.get('criteria_txt')
    )

    # Parse area
    area = handle_missing_area(site.get('area_hectares'))

    return {
        'category': category,
        'criteria': criteria,
        'area': area
    }
