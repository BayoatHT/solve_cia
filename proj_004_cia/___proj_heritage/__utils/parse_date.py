"""
Date parsing utilities for World Heritage data.

Handles inscription dates, secondary dates, and temporal data.
"""

from typing import Optional, List, Dict


def parse_date(date_str: Optional[str]) -> Optional[int]:
    """
    Parse date string to integer year.

    Args:
        date_str: Date string (e.g., "1992")

    Returns:
        Integer year or None if invalid

    Example:
        >>> parse_date("1992")
        1992

        >>> parse_date(None)
        None
    """
    if not date_str:
        return None

    try:
        return int(date_str)
    except (ValueError, TypeError):
        return None


def parse_secondary_dates(secondary_dates_str: Optional[str]) -> List[int]:
    """
    Parse comma-separated secondary dates.

    Args:
        secondary_dates_str: Comma-separated years (e.g., "1992, 1999, 2005")

    Returns:
        List of integer years, sorted

    Example:
        >>> parse_secondary_dates("1992, 1999")
        [1992, 1999]

        >>> parse_secondary_dates("")
        []
    """
    if not secondary_dates_str or secondary_dates_str.strip() == "":
        return []

    dates = []
    for date_part in secondary_dates_str.split(','):
        date_part = date_part.strip()
        if date_part:
            try:
                dates.append(int(date_part))
            except ValueError:
                continue

    return sorted(dates)


def parse_inscription_dates(date_inscribed: str, secondary_dates: str = None) -> Dict:
    """
    Parse inscription and extension dates into structured format.

    Args:
        date_inscribed: Primary inscription date
        secondary_dates: Secondary/extension dates

    Returns:
        Dictionary with primary, all dates, extensions, and timeline

    Example:
        >>> parse_inscription_dates("1992", "1992, 1999, 2005")
        {
            'primary_date': 1992,
            'all_dates': [1992, 1999, 2005],
            'extensions': [1999, 2005],
            'timeline': [
                {'year': 1992, 'event': 'Inscribed'},
                {'year': 1999, 'event': 'Extended'},
                {'year': 2005, 'event': 'Extended'}
            ]
        }
    """
    primary = parse_date(date_inscribed)

    if primary is None:
        return {
            'primary_date': None,
            'all_dates': [],
            'extensions': [],
            'timeline': []
        }

    # Parse secondary dates
    all_dates = parse_secondary_dates(secondary_dates) if secondary_dates else [primary]

    # Ensure primary is in the list
    if primary not in all_dates:
        all_dates.append(primary)

    all_dates = sorted(all_dates)

    # Identify extensions (dates after primary)
    extensions = [d for d in all_dates if d > primary]

    # Build timeline
    timeline = [{'year': primary, 'event': 'Inscribed'}]
    for ext_date in extensions:
        timeline.append({'year': ext_date, 'event': 'Extended'})

    return {
        'primary_date': primary,
        'all_dates': all_dates,
        'extensions': extensions,
        'timeline': timeline,
        'extension_count': len(extensions)
    }


def validate_year(year: int, min_year: int = 1900, max_year: int = 2030) -> bool:
    """
    Validate that a year is within reasonable range.

    Args:
        year: Year to validate
        min_year: Minimum valid year (default: 1900)
        max_year: Maximum valid year (default: 2030)

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_year(1992)
        True

        >>> validate_year(1800)
        False
    """
    if year is None:
        return False

    return min_year <= year <= max_year


def get_inscription_age(inscription_year: int, reference_year: int = None) -> int:
    """
    Calculate age of site inscription.

    Args:
        inscription_year: Year site was inscribed
        reference_year: Reference year (default: current year)

    Returns:
        Number of years since inscription

    Example:
        >>> get_inscription_age(1992, 2024)
        32
    """
    if reference_year is None:
        from datetime import datetime
        reference_year = datetime.now().year

    return reference_year - inscription_year


def format_date_range(dates: List[int]) -> str:
    """
    Format list of dates as range string.

    Args:
        dates: List of years

    Returns:
        Formatted date range string

    Example:
        >>> format_date_range([1992])
        '1992'

        >>> format_date_range([1992, 1999, 2005])
        '1992, 1999, 2005'

        >>> format_date_range([1992, 1993, 1994, 1995])
        '1992-1995'
    """
    if not dates:
        return ""

    if len(dates) == 1:
        return str(dates[0])

    # Check if consecutive
    is_consecutive = all(
        dates[i + 1] - dates[i] == 1
        for i in range(len(dates) - 1)
    )

    if is_consecutive and len(dates) > 2:
        return f"{dates[0]}-{dates[-1]}"

    return ", ".join(str(d) for d in dates)
