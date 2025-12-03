"""
Criteria parsing utilities for World Heritage data.

Handles cultural (i-vi) and natural (vii-x) criteria parsing.
"""

from typing import Optional, List, Dict


def parse_criteria_string(criteria_str: Optional[str], criteria_type: str = 'cultural') -> List[int]:
    """
    Parse criteria string to list of criterion numbers.

    Args:
        criteria_str: Comma-separated criteria (e.g., "c1, c2, c3" or "n7, n8")
        criteria_type: Type of criteria ('cultural' or 'natural')

    Returns:
        List of criterion numbers

    Example:
        >>> parse_criteria_string("c1, c2, c3")
        [1, 2, 3]

        >>> parse_criteria_string("n7, n8, n10")
        [7, 8, 10]

        >>> parse_criteria_string(None)
        []
    """
    if not criteria_str:
        return []

    numbers = []
    prefix = 'c' if criteria_type == 'cultural' else 'n'

    for criterion in criteria_str.split(','):
        criterion = criterion.strip().lower()

        # Extract number from criterion (e.g., "c1" -> 1, "n7" -> 7)
        if criterion.startswith(prefix):
            try:
                num = int(criterion[1:])
                numbers.append(num)
            except ValueError:
                continue

    return sorted(numbers)


def parse_criteria(
    cultural_criteria: Optional[str],
    natural_criteria: Optional[str],
    criteria_txt: Optional[str] = None
) -> Dict:
    """
    Parse all criteria into structured format.

    Args:
        cultural_criteria: Cultural criteria string (e.g., "c1, c2, c3")
        natural_criteria: Natural criteria string (e.g., "n7, n8")
        criteria_txt: Display text (e.g., "(i)(ii)(iii)")

    Returns:
        Dictionary with structured criteria data

    Example:
        >>> parse_criteria("c1, c2, c3", None, "(i)(ii)(iii)")
        {
            'cultural': [1, 2, 3],
            'natural': [],
            'all': [1, 2, 3],
            'display': '(i)(ii)(iii)',
            'count': 3,
            'type': 'Cultural'
        }

        >>> parse_criteria("c3", "n7, n9", "(iii)(vii)(ix)")
        {
            'cultural': [3],
            'natural': [7, 9],
            'all': [3, 7, 9],
            'display': '(iii)(vii)(ix)',
            'count': 3,
            'type': 'Mixed'
        }
    """
    cultural = parse_criteria_string(cultural_criteria, 'cultural')
    natural = parse_criteria_string(natural_criteria, 'natural')

    all_criteria = cultural + natural
    count = len(all_criteria)

    # Determine type
    if cultural and natural:
        site_type = 'Mixed'
    elif cultural:
        site_type = 'Cultural'
    elif natural:
        site_type = 'Natural'
    else:
        site_type = 'Unknown'

    return {
        'cultural': cultural,
        'natural': natural,
        'all': all_criteria,
        'display': criteria_txt or '',
        'count': count,
        'type': site_type
    }


def criteria_to_roman(criteria: List[int], criteria_type: str = 'cultural') -> str:
    """
    Convert criteria numbers to Roman numeral display.

    Args:
        criteria: List of criterion numbers
        criteria_type: Type ('cultural' for i-vi, 'natural' for vii-x)

    Returns:
        Roman numeral string (e.g., "(i)(ii)(iii)")

    Example:
        >>> criteria_to_roman([1, 2, 3], 'cultural')
        '(i)(ii)(iii)'

        >>> criteria_to_roman([7, 8], 'natural')
        '(vii)(viii)'
    """
    roman_map = {
        1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v', 6: 'vi',
        7: 'vii', 8: 'viii', 9: 'ix', 10: 'x'
    }

    return ''.join(f'({roman_map.get(c, "")})' for c in sorted(criteria))


def get_criteria_descriptions(criteria_numbers: List[int], criteria_type: str) -> List[Dict]:
    """
    Get detailed descriptions for criteria.

    Args:
        criteria_numbers: List of criterion numbers
        criteria_type: 'cultural' or 'natural'

    Returns:
        List of dictionaries with number, roman, and description

    Example:
        >>> get_criteria_descriptions([1, 2], 'cultural')
        [
            {
                'number': 1,
                'roman': '(i)',
                'code': 'c1',
                'description': 'Masterpiece of human creative genius'
            },
            {
                'number': 2,
                'roman': '(ii)',
                'code': 'c2',
                'description': 'Interchange of human values'
            }
        ]
    """
    descriptions_map = {
        'cultural': {
            1: 'Masterpiece of human creative genius',
            2: 'Interchange of human values',
            3: 'Testimony to cultural tradition',
            4: 'Significant stage in human history',
            5: 'Traditional human settlement',
            6: 'Associated with events or traditions',
        },
        'natural': {
            7: 'Natural beauty or phenomena',
            8: 'Geological or geomorphic features',
            9: 'Ecological processes',
            10: 'Biodiversity and species conservation',
        }
    }

    roman_map = {
        1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v', 6: 'vi',
        7: 'vii', 8: 'viii', 9: 'ix', 10: 'x'
    }

    prefix = 'c' if criteria_type == 'cultural' else 'n'
    descriptions = descriptions_map.get(criteria_type, {})

    result = []
    for num in sorted(criteria_numbers):
        result.append({
            'number': num,
            'roman': f'({roman_map.get(num, "")})',
            'code': f'{prefix}{num}',
            'description': descriptions.get(num, 'Unknown criterion')
        })

    return result


def validate_criteria(criteria_numbers: List[int], criteria_type: str) -> bool:
    """
    Validate that criteria numbers are valid for the type.

    Args:
        criteria_numbers: List of criterion numbers
        criteria_type: 'cultural' or 'natural'

    Returns:
        True if all criteria are valid, False otherwise

    Example:
        >>> validate_criteria([1, 2, 3], 'cultural')
        True

        >>> validate_criteria([7, 8], 'cultural')  # Natural criteria for cultural type
        False

        >>> validate_criteria([1, 7], 'mixed')  # Not a valid type
        False
    """
    if criteria_type == 'cultural':
        valid_range = range(1, 7)  # i-vi
    elif criteria_type == 'natural':
        valid_range = range(7, 11)  # vii-x
    else:
        return False

    return all(c in valid_range for c in criteria_numbers)
