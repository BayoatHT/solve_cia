import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_marine_fisheries(fisheries_data: dict, iso3Code: str = None, return_original: bool = False) -> dict:
    """
    Parse marine fisheries from CIA Environment section for a given country.

    Args:
        fisheries_data: The 'Marine fisheries' section data
        iso3Code: ISO3 country code for logging purposes
        return_original: If True, return raw data without parsing

    Returns:
        Dictionary with structured marine fisheries data
    """
    result = {
        "marine_fisheries": {
            "description": None,
            "total_catch_mt": None,
            "year": None,
            "regional_bodies": None,
            "major_producers": [],
            "principal_catches": []
        },
        "marine_fisheries_note": ""
    }

    if return_original:
        return fisheries_data

    if not fisheries_data or not isinstance(fisheries_data, dict):
        return result

    text = fisheries_data.get('text', '')
    if text and text.upper() != 'NA':
        cleaned = clean_text(text)
        result['marine_fisheries']['description'] = cleaned

        # Try to extract total catch
        catch_match = re.search(r'total catch of ([\d,]+)\s*mt', cleaned, re.IGNORECASE)
        if catch_match:
            result['marine_fisheries']['total_catch_mt'] = int(catch_match.group(1).replace(',', ''))

        # Try to extract year
        year_match = re.search(r'in (\d{4})', cleaned)
        if year_match:
            result['marine_fisheries']['year'] = year_match.group(1)

        # Try to extract regional fisheries bodies
        bodies_match = re.search(r'Regional fisheries bodies:\s*(.+?)(?:\.|$)', cleaned, re.IGNORECASE)
        if bodies_match:
            result['marine_fisheries']['regional_bodies'] = bodies_match.group(1).strip()

        # Try to extract major producers with catch amounts
        producer_pattern = re.compile(r'([A-Za-z\s]+)\s*\(([\d,]+)\s*mt\)', re.IGNORECASE)
        producers = producer_pattern.findall(cleaned)
        for name, catch in producers[:10]:  # Limit to first 10
            name = name.strip()
            if name and len(name) > 2:
                result['marine_fisheries']['major_producers'].append({
                    'country': name,
                    'catch_mt': int(catch.replace(',', ''))
                })

    return result


if __name__ == "__main__":
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

    print("="*60)
    print("Testing parse_marine_fisheries")
    print("="*60)
    # Marine fisheries primarily in Oceans data - test ocean codes
    for iso3 in ['XXX', 'ATL', 'PAC', 'IND', 'USA', 'CHN']:
        print(f"\n{iso3}:")
        try:
            raw_data = load_country_data(iso3)
            fisheries_data = raw_data.get('Environment', {}).get('Marine fisheries', {})
            result = parse_marine_fisheries(fisheries_data, iso3)
            if result and result['marine_fisheries']['description']:
                mf = result['marine_fisheries']
                if mf['total_catch_mt']:
                    print(f"  Total catch: {mf['total_catch_mt']:,} mt ({mf['year']})")
                if mf['major_producers']:
                    print(f"  Major producers: {len(mf['major_producers'])}")
                else:
                    print(f"  Description: {mf['description'][:60]}...")
            else:
                print("  No marine fisheries data")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
