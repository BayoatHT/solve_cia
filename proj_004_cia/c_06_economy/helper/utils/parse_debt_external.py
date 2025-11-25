import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_06_economy.helper.utils.parse_econ_value import parse_econ_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_debt_external(iso3Code: str) -> dict:
    """
    Parse external debt data from CIA World Factbook for a given country.

    This parser extracts external debt information including:
    - Multi-year historical data
    - Latest value and year
    - Dollar values with estimate status
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured external debt data:
        {
            "external_debt_data": [{"year": int, "value": float, "unit": str, "is_estimate": bool}],
            "external_debt_latest_value": float,
            "external_debt_latest_year": int,
            "external_debt_unit": str,
            "external_debt_note": str
        }

    Examples:
        >>> data = parse_debt_external('USA')
        >>> 'external_debt_latest_year' in data
        True

        >>> data = parse_debt_external('CHN')
        >>> isinstance(data.get('external_debt_data', []), list)
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Debt - external
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Debt - external', {})

    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        yearly_data = []
        for k, v in pass_data.items():
            if k == 'note':
                if isinstance(v, str) and v.strip():
                    result['external_debt_note'] = clean_text(v)
                continue
            if isinstance(v, dict) and 'text' in v:
                year_match = re.search(r'(\d{4})', k)
                if year_match:
                    year = int(year_match.group(1))
                    text = v.get('text', '')
                    if text:
                        parsed = parse_econ_value(text)
                        entry = {'year': year}
                        if parsed['value'] is not None:
                            entry['value'] = parsed['value']
                        if parsed['unit']:
                            entry['unit'] = parsed['unit']
                        if parsed['is_estimate']:
                            entry['is_estimate'] = parsed['is_estimate']
                        yearly_data.append(entry)
        if yearly_data:
            yearly_data.sort(key=lambda x: x['year'], reverse=True)
            result['external_debt_data'] = yearly_data
            if yearly_data[0].get('value') is not None:
                result['external_debt_latest_value'] = yearly_data[0]['value']
            result['external_debt_latest_year'] = yearly_data[0]['year']
            if yearly_data[0].get('unit'):
                result['external_debt_unit'] = yearly_data[0]['unit']
    except Exception as e:
        logger.error(f"Error parsing debt_external for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_debt_external with real country data."""
    print("="*60)
    print("Testing parse_debt_external across countries")
    print("="*60)

    test_countries = ['USA', 'CHN', 'BRA', 'IND', 'ZAF', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_debt_external(iso3)

            if result.get('external_debt_latest_value') is not None:
                latest = result['external_debt_latest_value']
                year = result.get('external_debt_latest_year', '')

                # Format large numbers
                if abs(latest) >= 1e12:
                    display = f"${latest/1e12:.2f}T"
                elif abs(latest) >= 1e9:
                    display = f"${latest/1e9:.2f}B"
                elif abs(latest) >= 1e6:
                    display = f"${latest/1e6:.2f}M"
                else:
                    display = f"${latest:,.0f}"

                print(f"  External Debt: {display} ({year})")

                if result.get('external_debt_data'):
                    data_count = len(result['external_debt_data'])
                    if data_count > 1:
                        print(f"  Historical data: {data_count} years")
            else:
                print("  No external debt data found")

            if result.get('external_debt_note'):
                note = result['external_debt_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
