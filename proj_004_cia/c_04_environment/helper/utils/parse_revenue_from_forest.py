import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_revenue_from_forest(iso3Code: str) -> dict:
    """Parse revenue from forest resources from CIA Environment section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    environment_section = raw_data.get('Environment', {})
    forest_data = environment_section.get('Revenue from forest resources', {})

    if not forest_data:
        return result

    result = {
        "revenue_forest": {
            "value": None,
            "unit": "% of GDP",
            "timestamp": None,
            "is_estimate": False
        },
        "revenue_forest_note": ""
    }

    text = forest_data.get('text', '')
    if text and text.upper() != 'NA':
        # Extract percentage
        pct_match = re.search(r'([\d.]+)%', text)
        if pct_match:
            result['revenue_forest']['value'] = float(pct_match.group(1))

        # Extract year
        year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)
        if year_match:
            result['revenue_forest']['timestamp'] = year_match.group(1)
            result['revenue_forest']['is_estimate'] = 'est' in text.lower()

    return result


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_revenue_from_forest")
    print("="*60)
    for iso3 in ['USA', 'BRA', 'CAN', 'RUS', 'COD']:
        print(f"\n{iso3}:")
        try:
            result = parse_revenue_from_forest(iso3)
            if result:
                print(f"  {result}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
