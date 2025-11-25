import re
import logging
from typing import Dict, Any
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_remittances(iso3Code: str, return_original: bool = False)-> Dict[str, Any]:
    """
    Parse remittances data from CIA World Factbook for a given country.

    This parser extracts remittances information including:
    - Multi-year percentage of GDP data
    - Latest value and year
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured remittances data:
        {
            "remittances_data": [{"year": int, "percentage_of_gdp": float}],
            "remittances_latest_value": float,
            "remittances_latest_year": int,
            "remittances_note": str
        }

    Examples:
        >>> data = parse_remittances('IND')
        >>> 'remittances_latest_year' in data
        True

        >>> data = parse_remittances('PHL')
        >>> isinstance(data.get('remittances_data', []), list)
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Remittances
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Remittances', {})

    if return_original:
        return pass_data


    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        yearly_data = []
        for key, value in pass_data.items():
            if key == "note":
                # Process 'note' field
                result["remittances_note"] = clean_text(value)
                continue

            # Extract the year from the key
            year_match = re.search(r'\d{4}', key)
            if not year_match:
                logger.warning(f"No year found in key: {key}")
                continue

            year = int(year_match.group(0))

            # Process 'text' field for percentage and year
            text = value.get("text", "")
            match = re.match(r"([\d.]+)% of GDP \((\d{4})", text)
            if match:
                percentage = float(match.group(1))
                yearly_data.append({
                    "year": year,
                    "percentage_of_gdp": percentage
                })
            else:
                logger.warning(f"Unexpected format in 'text' data: {text}")

        if yearly_data:
            yearly_data.sort(key=lambda x: x['year'], reverse=True)
            result['remittances_data'] = yearly_data
            result['remittances_latest_value'] = yearly_data[0]['percentage_of_gdp']
            result['remittances_latest_year'] = yearly_data[0]['year']

    except Exception as e:
        logger.error(f"Error parsing remittances for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_remittances with real country data."""
    print("="*60)
    print("Testing parse_remittances across countries")
    print("="*60)

    test_countries = ['IND', 'PHL', 'MEX', 'EGY', 'PAK', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_remittances(iso3)

            if result.get('remittances_latest_value') is not None:
                latest = result['remittances_latest_value']
                year = result.get('remittances_latest_year', '')
                print(f"  Remittances: {latest}% of GDP ({year})")

                if result.get('remittances_data'):
                    data_count = len(result['remittances_data'])
                    if data_count > 1:
                        print(f"  Historical data: {data_count} years")
            else:
                print("  No remittances data found")

            if result.get('remittances_note'):
                note = result['remittances_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
