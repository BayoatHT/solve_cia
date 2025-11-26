import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_revenue_from_coal(coal_data: dict, iso3Code: str = None, return_original: bool = False) -> dict:
    """
    Parse revenue from coal from CIA Environment section for a given country.

    Args:
        coal_data: The 'Revenue from coal' section data
        iso3Code: ISO3 country code for logging purposes
        return_original: If True, return raw data without parsing

    Returns:
        Dictionary with structured coal revenue data
    """
    if return_original:
        return coal_data

    if not coal_data:
        return {}

    result = {
        "revenue_coal": {
            "value": None,
            "unit": "% of GDP",
            "timestamp": None,
            "is_estimate": False
        },
        "revenue_coal_note": ""
    }

    text = coal_data.get('text', '')
    if text and text.upper() != 'NA':
        pct_match = re.search(r'([\d.]+)%', text)
        if pct_match:
            result['revenue_coal']['value'] = float(pct_match.group(1))

        year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)
        if year_match:
            result['revenue_coal']['timestamp'] = year_match.group(1)
            result['revenue_coal']['is_estimate'] = 'est' in text.lower()

    return result


if __name__ == "__main__":
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

    print("="*60)
    print("Testing parse_revenue_from_coal")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'IND', 'RUS', 'AUS']:
        print(f"\n{iso3}:")
        try:
            raw_data = load_country_data(iso3)
            coal_data = raw_data.get('Environment', {}).get('Revenue from coal', {})
            result = parse_revenue_from_coal(coal_data, iso3)
            if result:
                print(f"  {result}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
