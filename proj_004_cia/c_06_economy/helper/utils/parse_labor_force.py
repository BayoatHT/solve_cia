import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_06_economy.helper.utils.parse_econ_value import parse_econ_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_labor_force(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse labor force data from CIA World Factbook for a given country.

    This parser extracts labor force data including:
    - Multi-year historical data
    - Latest value and year
    - Numeric labor force values
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured labor force data:
        {
            "labor_force_value": float,
            "labor_force_unit": str,
            "labor_force_year": int,
            "labor_force_is_estimate": bool,
            "labor_force_note": str
        }

    Examples:
        >>> data = parse_labor_force('USA')
        >>> 'labor_force_value' in data
        True

        >>> data = parse_labor_force('CHN')
        >>> data.get('labor_force_year') > 2000
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Labor force
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Labor force', {})

    if return_original:
        return pass_data


    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        # Handle simple text/note structure
        if 'text' in pass_data:
            text = pass_data.get('text', '')
            if text:
                parsed = parse_econ_value(text)
                if parsed['value'] is not None:
                    result['labor_force_value'] = parsed['value']
                if parsed['unit']:
                    result['labor_force_unit'] = parsed['unit']
                if parsed['is_estimate']:
                    result['labor_force_is_estimate'] = parsed['is_estimate']
                # Extract year from text if present
                year_match = re.search(r'\((\d{4})', text)
                if year_match:
                    result['labor_force_year'] = int(year_match.group(1))

        if 'note' in pass_data:
            note = pass_data['note']
            if isinstance(note, str) and note.strip():
                result['labor_force_note'] = clean_text(note)
    except Exception as e:
        logger.error(f"Error parsing labor_force for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_labor_force with real country data."""
    print("="*60)
    print("Testing parse_labor_force across countries")
    print("="*60)

    test_countries = ['USA', 'CHN', 'IND', 'BRA', 'RUS', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_labor_force(iso3)

            if result.get('labor_force_value') is not None:
                value = result['labor_force_value']
                year = result.get('labor_force_year', '')
                unit = result.get('labor_force_unit', '')

                # Format large numbers
                if value >= 1e9:
                    display = f"{value/1e9:.2f}B"
                elif value >= 1e6:
                    display = f"{value/1e6:.2f}M"
                elif value >= 1e3:
                    display = f"{value/1e3:.2f}K"
                else:
                    display = f"{value:,.0f}"

                year_str = f" ({year})" if year else ""
                est_str = " (est.)" if result.get('labor_force_is_estimate') else ""
                print(f"  Labor Force: {display}{year_str}{est_str}")
            else:
                print("  No labor force data found")

            if result.get('labor_force_note'):
                note = result['labor_force_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
