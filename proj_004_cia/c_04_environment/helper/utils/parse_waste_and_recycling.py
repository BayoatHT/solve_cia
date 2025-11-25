import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_waste_and_recycling(iso3Code: str, return_original: bool = False)-> dict:
    """Parse waste and recycling from CIA Environment section for a given country."""
    result = {
        "waste_recycling": {
            "waste_generated": None,
            "waste_generated_unit": "tons",
            "waste_recycled": None,
            "waste_recycled_unit": "tons",
            "recycling_percent": None,
            "timestamp": None,
            "is_estimate": False
        },
        "waste_recycling_note": ""
    }

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    environment_section = raw_data.get('Environment', {})
    waste_data = environment_section.get('Waste and recycling', {})

    if return_original:
        return waste_data


    if not waste_data or not isinstance(waste_data, dict):
        return result

    def extract_value_and_year(text):
        if not text:
            return None, None, False
        value = None
        year = None
        is_est = False

        # Extract number with units like "258 million tons"
        num_match = re.search(r'([\d,.]+)\s*(million|billion|thousand)?', text)
        if num_match:
            value = float(num_match.group(1).replace(',', ''))
            multiplier = num_match.group(2)
            if multiplier == 'million':
                value *= 1_000_000
            elif multiplier == 'billion':
                value *= 1_000_000_000
            elif multiplier == 'thousand':
                value *= 1_000

        year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)
        if year_match:
            year = year_match.group(1)
            is_est = 'est' in text.lower()

        return value, year, is_est

    # Parse waste generated
    gen_data = waste_data.get('municipal solid waste generated annually', {})
    if gen_data and isinstance(gen_data, dict):
        text = gen_data.get('text', '')
        if text and text.upper() != 'NA':
            value, year, is_est = extract_value_and_year(text)
            result['waste_recycling']['waste_generated'] = value
            result['waste_recycling']['timestamp'] = year
            result['waste_recycling']['is_estimate'] = is_est

    # Parse waste recycled
    rec_data = waste_data.get('municipal solid waste recycled annually', {})
    if rec_data and isinstance(rec_data, dict):
        text = rec_data.get('text', '')
        if text and text.upper() != 'NA':
            value, _, _ = extract_value_and_year(text)
            result['waste_recycling']['waste_recycled'] = value

    # Parse recycling percentage
    pct_data = waste_data.get('percent of municipal solid waste recycled', {})
    if pct_data and isinstance(pct_data, dict):
        text = pct_data.get('text', '')
        if text and text.upper() != 'NA':
            pct_match = re.search(r'([\d.]+)%', text)
            if pct_match:
                result['waste_recycling']['recycling_percent'] = float(pct_match.group(1))

    return result


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_waste_and_recycling")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'DEU', 'JPN', 'GBR', 'FRA']:
        print(f"\n{iso3}:")
        try:
            result = parse_waste_and_recycling(iso3)
            if result and result['waste_recycling']['waste_generated']:
                wr = result['waste_recycling']
                gen = wr['waste_generated'] / 1e6 if wr['waste_generated'] else 0
                pct = wr['recycling_percent']
                print(f"  Generated: {gen:,.1f} million tons")
                print(f"  Recycled: {pct}%" if pct else "  Recycled: N/A")
                print(f"  Year: {wr['timestamp']}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
