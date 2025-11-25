import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_gdp_official_exchange(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse GDP (official exchange rate) data from CIA World Factbook for a given country.

    This parser extracts GDP at official exchange rate information including:
    - Multi-year historical data
    - Latest value and year
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured GDP official exchange data:
        {
            "gdp_official_exchange_data": [{"year": int, "value": str}],
            "gdp_official_exchange_latest": str,
            "gdp_official_exchange_latest_year": int,
            "gdp_official_exchange": str,
            "gdp_official_exchange_note": str
        }

    Examples:
        >>> data = parse_gdp_official_exchange('USA')
        >>> 'gdp_official_exchange' in data
        True

        >>> data = parse_gdp_official_exchange('CHN')
        >>> 'gdp_official_exchange_latest_year' in data
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> GDP (official exchange rate)
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('GDP (official exchange rate)', {})

    if return_original:
        return pass_data


    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        yearly_data = []
        for k, v in pass_data.items():
            if isinstance(v, dict) and 'text' in v:
                year_match = re.search(r'(\d{4})', k)
                if year_match:
                    year = int(year_match.group(1))
                    text = v.get('text', '')
                    if text:
                        yearly_data.append({'year': year, 'value': clean_text(text)})
        if yearly_data:
            yearly_data.sort(key=lambda x: x['year'], reverse=True)
            result['gdp_official_exchange_data'] = yearly_data
            result['gdp_official_exchange_latest'] = yearly_data[0]['value']
            result['gdp_official_exchange_latest_year'] = yearly_data[0]['year']
        if 'text' in pass_data:
            result['gdp_official_exchange'] = clean_text(pass_data['text'])
        if 'note' in pass_data:
            note = pass_data['note']
            if isinstance(note, str) and note.strip():
                result['gdp_official_exchange_note'] = clean_text(note)
    except Exception as e:
        logger.error(f"Error parsing gdp_official_exchange for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_gdp_official_exchange with real country data."""
    print("="*60)
    print("Testing parse_gdp_official_exchange across countries")
    print("="*60)

    test_countries = ['USA', 'CHN', 'DEU', 'JPN', 'IND', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_gdp_official_exchange(iso3)

            if result.get('gdp_official_exchange'):
                gdp = result['gdp_official_exchange']
                print(f"  GDP (Official Exchange Rate): {gdp}")
            elif result.get('gdp_official_exchange_latest'):
                gdp = result['gdp_official_exchange_latest']
                year = result.get('gdp_official_exchange_latest_year', '')
                print(f"  GDP (Official Exchange Rate): {gdp} ({year})")
            else:
                print("  No GDP official exchange rate data found")

            if result.get('gdp_official_exchange_note'):
                note = result['gdp_official_exchange_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
