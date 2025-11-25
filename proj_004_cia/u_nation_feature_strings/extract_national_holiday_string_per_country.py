"""Extract national_holiday for each country."""

from typing import Dict
from proj_004_cia.u_nation_feature_strings.base_extractor import extract_string_feature
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data


def parse_national_holiday(raw_data: Dict, iso3Code: str) -> Dict:
    """Parse national_holiday from raw data."""
    gov_section = raw_data.get('Government', {})
    field_data = gov_section.get('National holiday', {})

    return {
        'national_holiday': field_data.get('text', '').strip() if isinstance(field_data, dict) else ''
    }


def extract_national_holiday(parsed_data: Dict) -> str:
    """Extract national_holiday from parsed data."""
    return parsed_data.get('national_holiday', '')


def get_national_holiday(verbose: bool = False) -> Dict[str, str]:
    """
    Get national_holiday for all countries.

    Args:
        verbose: If True, print extraction statistics

    Returns:
        Dictionary mapping ISO3 codes to national_holiday values

    Example:
        >>> data = get_national_holiday()
        >>> data['USA']
        'Independence Day, 4 July (1776)'
    """
    return extract_string_feature(
        parse_national_holiday,
        extract_national_holiday,
        'national_holiday',
        verbose=verbose
    )


if __name__ == "__main__":
    data = get_national_holiday(verbose=True)

    print("\nSample results:")
    for iso3 in ['USA', 'FRA', 'CHN', 'BRA', 'GBR']:
        val = data.get(iso3, 'N/A')
        display = f"{val[:80]}..." if len(val) > 80 else val
        print(f"  {iso3}: {display}")
