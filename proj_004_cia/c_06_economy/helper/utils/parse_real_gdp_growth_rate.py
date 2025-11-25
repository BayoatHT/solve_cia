import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_06_economy.helper.utils.parse_econ_value import parse_econ_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_real_gdp_growth_rate(iso3Code: str) -> dict:
    """
    Parse real GDP growth rate data from CIA World Factbook for a given country.

    This parser extracts real GDP growth rate data including:
    - Multi-year historical data
    - Latest value and year
    - Percentage growth rates with estimate status
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured GDP growth rate data:
        {
            "gdp_growth_data": [{"year": int, "value": float, "unit": str, "is_estimate": bool}],
            "gdp_growth_latest_value": float,
            "gdp_growth_latest_year": int,
            "gdp_growth_unit": str,
            "gdp_growth_note": str
        }

    Examples:
        >>> data = parse_real_gdp_growth_rate('USA')
        >>> 'gdp_growth_latest_year' in data
        True

        >>> data = parse_real_gdp_growth_rate('CHN')
        >>> isinstance(data.get('gdp_growth_data', []), list)
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Real GDP growth rate
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Real GDP growth rate', {})

    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        yearly_data = []
        for k, v in pass_data.items():
            if k == 'note':
                if isinstance(v, str) and v.strip():
                    result['gdp_growth_note'] = clean_text(v)
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
            result['gdp_growth_data'] = yearly_data
            if yearly_data[0].get('value') is not None:
                result['gdp_growth_latest_value'] = yearly_data[0]['value']
            result['gdp_growth_latest_year'] = yearly_data[0]['year']
            if yearly_data[0].get('unit'):
                result['gdp_growth_unit'] = yearly_data[0]['unit']
    except Exception as e:
        logger.error(f"Error parsing real_gdp_growth_rate for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_real_gdp_growth_rate with real country data."""
    print("="*60)
    print("Testing parse_real_gdp_growth_rate across countries")
    print("="*60)

    test_countries = ['USA', 'CHN', 'IND', 'BRA', 'RUS', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_real_gdp_growth_rate(iso3)

            if result.get('gdp_growth_latest_value') is not None:
                latest = result['gdp_growth_latest_value']
                year = result.get('gdp_growth_latest_year', '')
                unit = result.get('gdp_growth_unit', '%')
                print(f"  Latest: {latest}{unit} ({year})")

                if result.get('gdp_growth_data'):
                    data_count = len(result['gdp_growth_data'])
                    if data_count > 1:
                        print(f"  Historical data: {data_count} years")
                        # Show last 3 years
                        for entry in result['gdp_growth_data'][:3]:
                            val = entry.get('value', 'N/A')
                            yr = entry.get('year', '')
                            est = " (est.)" if entry.get('is_estimate') else ""
                            print(f"    {yr}: {val}%{est}")
            else:
                print("  No GDP growth data found")

            if result.get('gdp_growth_note'):
                note = result['gdp_growth_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
