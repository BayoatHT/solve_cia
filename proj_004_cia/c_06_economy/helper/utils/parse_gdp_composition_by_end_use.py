import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

KEY_MAPPING = {
    "exports of goods and services": "gdp_exports",
    "government consumption": "gdp_govt_consumption",
    "household consumption": "gdp_household_consumption",
    "imports of goods and services": "gdp_imports",
    "investment in fixed capital": "gdp_investment_fixed_capital",
    "investment in inventories": "gdp_investment_inventories"
}

def parse_gdp_composition_by_end_use(iso3Code: str, return_original: bool = False)-> dict:
    """Parse GDP composition by end use data from CIA World Factbook for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result
    
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('GDP - composition, by end use', {})

    if return_original:
        return pass_data

    if not pass_data or not isinstance(pass_data, dict):
        return result
    
    try:
        for key, mapped_key in KEY_MAPPING.items():
            data = pass_data.get(key, {})
            text = data.get("text", "")
            if text:
                if 'NA' in text.upper():
                    year_match = re.search(r'\((\d{4})', text)
                    result[mapped_key] = {"value": None, "unit": "%", "year": int(year_match.group(1)) if year_match else None, "note": "NA"}
                    continue
                value_match = re.match(r"(-?[\d.]+)%\s+\((\d{4})", text)
                if value_match:
                    result[mapped_key] = {"value": float(value_match.group(1)), "unit": "%", "year": int(value_match.group(2))}
        if "note" in pass_data:
            result["gdp_composition_note"] = clean_text(pass_data["note"])
    except Exception as e:
        logger.error(f"Error parsing gdp_composition_by_end_use for {iso3Code}: {e}")
    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_gdp_composition_by_end_use")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'DEU', 'IND', 'BRA', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_gdp_composition_by_end_use(iso3)
            if result:
                for key, val in result.items():
                    if key != 'gdp_composition_note' and isinstance(val, dict):
                        print(f"  {key}: {val.get('value')}% ({val.get('year')})" if val.get('value') else f"  {key}: N/A")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
