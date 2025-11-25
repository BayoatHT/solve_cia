import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_06_economy.helper.utils.parse_econ_value import parse_econ_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_gdp_per_capita_ppp(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse GDP per capita PPP data from CIA World Factbook for a given country.

    This parser extracts GDP per capita purchasing power parity data including:
    - Multi-year historical data
    - Latest value and year
    - Currency values with estimate status
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured GDP per capita PPP data:
        {
            "gdp_per_capita_ppp_data": [{"year": int, "value": float, "unit": str, "is_estimate": bool}],
            "gdp_per_capita_ppp_latest_value": float,
            "gdp_per_capita_ppp_latest_year": int,
            "gdp_per_capita_ppp_unit": str,
            "gdp_per_capita_ppp_note": str
        }

    Examples:
        >>> data = parse_gdp_per_capita_ppp('USA')
        >>> 'gdp_per_capita_ppp_latest_year' in data
        True

        >>> data = parse_gdp_per_capita_ppp('CHN')
        >>> isinstance(data.get('gdp_per_capita_ppp_data', []), list)
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Real GDP per capita
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Real GDP per capita', {})

    if return_original:
        return pass_data


    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        yearly_data = []
        for k, v in pass_data.items():
            if k == 'note':
                if isinstance(v, str) and v.strip():
                    result['gdp_per_capita_ppp_note'] = clean_text(v)
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
            result['gdp_per_capita_ppp_data'] = yearly_data
            if yearly_data[0].get('value') is not None:
                result['gdp_per_capita_ppp_latest_value'] = yearly_data[0]['value']
            result['gdp_per_capita_ppp_latest_year'] = yearly_data[0]['year']
            if yearly_data[0].get('unit'):
                result['gdp_per_capita_ppp_unit'] = yearly_data[0]['unit']
    except Exception as e:
        logger.error(f"Error parsing gdp_per_capita_ppp for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_gdp_per_capita_ppp with real country data."""
    print("="*60)
    print("Testing parse_gdp_per_capita_ppp across countries")
    print("="*60)

    test_countries = ['USA', 'CHN', 'IND', 'BRA', 'DEU', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_gdp_per_capita_ppp(iso3)

            if result.get('gdp_per_capita_ppp_latest_value') is not None:
                latest = result['gdp_per_capita_ppp_latest_value']
                year = result.get('gdp_per_capita_ppp_latest_year', '')
                unit = result.get('gdp_per_capita_ppp_unit', '$')

                # Format large numbers
                if latest >= 1000:
                    display = f"${latest:,.0f}"
                else:
                    display = f"${latest:.2f}"

                print(f"  Latest: {display} ({year})")

                if result.get('gdp_per_capita_ppp_data'):
                    data_count = len(result['gdp_per_capita_ppp_data'])
                    if data_count > 1:
                        print(f"  Historical data: {data_count} years")
                        # Show last 3 years
                        for entry in result['gdp_per_capita_ppp_data'][:3]:
                            val = entry.get('value', 'N/A')
                            yr = entry.get('year', '')
                            est = " (est.)" if entry.get('is_estimate') else ""
                            if isinstance(val, (int, float)) and val >= 1000:
                                val_str = f"${val:,.0f}"
                            else:
                                val_str = f"${val}"
                            print(f"    {yr}: {val_str}{est}")
            else:
                print("  No GDP per capita PPP data found")

            if result.get('gdp_per_capita_ppp_note'):
                note = result['gdp_per_capita_ppp_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
