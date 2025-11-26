import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_urbanization(urban_data: dict, iso3Code: str = None, return_original: bool = False) -> dict:
    """
    Parse urbanization from CIA Environment section for a given country.

    Args:
        urban_data: The 'Urbanization' section data
        iso3Code: ISO3 country code for logging purposes
        return_original: If True, return raw data without parsing

    Returns:
        Dictionary with structured urbanization data
    """
    result = {
        "env_urbanization": {
            "urban_population_percent": None,
            "urban_population_year": None,
            "rate_of_urbanization": None,
            "rate_period": None,
            "is_estimate": False
        },
        "env_urbanization_note": ""
    }

    if return_original:
        return urban_data

    if not urban_data or not isinstance(urban_data, dict):
        return result

    # Parse urban population
    pop_data = urban_data.get('urban population', {})
    if pop_data and isinstance(pop_data, dict):
        text = pop_data.get('text', '')
        if text and text.upper() != 'NA':
            pct_match = re.search(r'([\d.]+)%', text)
            if pct_match:
                result['env_urbanization']['urban_population_percent'] = float(pct_match.group(1))
            year_match = re.search(r'\((\d{4})\)', text)
            if year_match:
                result['env_urbanization']['urban_population_year'] = year_match.group(1)

    # Parse rate of urbanization
    rate_data = urban_data.get('rate of urbanization', {})
    if rate_data and isinstance(rate_data, dict):
        text = rate_data.get('text', '')
        if text and text.upper() != 'NA':
            rate_match = re.search(r'(-?[\d.]+)%', text)
            if rate_match:
                result['env_urbanization']['rate_of_urbanization'] = float(rate_match.group(1))
            period_match = re.search(r'\((\d{4}-\d{2,4})\s*(est\.?)?\)', text)
            if period_match:
                result['env_urbanization']['rate_period'] = period_match.group(1)
                result['env_urbanization']['is_estimate'] = 'est' in text.lower()

    note = urban_data.get('note', '')
    if note:
        result['env_urbanization_note'] = clean_text(note) if isinstance(note, str) else clean_text(note.get('text', ''))

    return result


if __name__ == "__main__":
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

    print("="*60)
    print("Testing parse_urbanization")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'IND', 'BRA', 'RUS', 'DEU']:
        print(f"\n{iso3}:")
        try:
            raw_data = load_country_data(iso3)
            urban_data = raw_data.get('Environment', {}).get('Urbanization', {})
            result = parse_urbanization(urban_data, iso3)
            if result and result['env_urbanization']['urban_population_percent']:
                eu = result['env_urbanization']
                print(f"  Urban pop: {eu['urban_population_percent']}% ({eu['urban_population_year']})")
                print(f"  Rate: {eu['rate_of_urbanization']}% ({eu['rate_period']})")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
