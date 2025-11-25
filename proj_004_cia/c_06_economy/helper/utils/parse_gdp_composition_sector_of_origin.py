import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

KEY_MAPPING = {"agriculture": "gdp_agriculture", "industry": "gdp_industry", "services": "gdp_services"}

def parse_gdp_composition_sector_of_origin(iso3Code: str, return_original: bool = False)-> dict:
    """Parse GDP composition by sector of origin data from CIA World Factbook."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result
    
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('GDP - composition, by sector of origin', {})

    if return_original:
        return pass_data

    if not pass_data or not isinstance(pass_data, dict):
        return result
    
    try:
        for key, mapped_key in KEY_MAPPING.items():
            data = pass_data.get(key, {})
            text = data.get("text", "")
            if text:
                if text.upper().strip() == 'NA' or text.upper().startswith('NA '):
                    result[mapped_key] = {"value": None, "unit": "%", "year": None, "note": "NA"}
                    continue
                match = re.match(r"(-?[\d.]+)%\s+\((\d{4})", text)
                fy_match = re.match(r"(-?[\d.]+)%\s+\(FY(\d{2})/(\d{2})", text)
                if match:
                    result[mapped_key] = {"value": float(match.group(1)), "unit": "%", "year": int(match.group(2))}
                elif fy_match:
                    fy_year = int(fy_match.group(2))
                    full_year = 2000 + fy_year if fy_year < 50 else 1900 + fy_year
                    result[mapped_key] = {"value": float(fy_match.group(1)), "unit": "%", "year": full_year,
                                         "fiscal_year": f"FY{fy_match.group(2)}/{fy_match.group(3)}"}
        if "note" in pass_data:
            result["gdp_composition_note"] = clean_text(pass_data["note"])
    except Exception as e:
        logger.error(f"Error parsing gdp_composition_sector_of_origin for {iso3Code}: {e}")
    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_gdp_composition_sector_of_origin")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'DEU', 'IND', 'BRA', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_gdp_composition_sector_of_origin(iso3)
            if result:
                for key in ['gdp_agriculture', 'gdp_industry', 'gdp_services']:
                    if key in result:
                        val = result[key]
                        print(f"  {key}: {val.get('value')}% ({val.get('year')})" if val.get('value') else f"  {key}: N/A")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
