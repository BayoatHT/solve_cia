import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Key mapping dictionary for clear output structure
KEY_MAPPING = {
    "agriculture": "gdp_agriculture",
    "industry": "gdp_industry",
    "services": "gdp_services"
}


def parse_gdp_composition_sector_of_origin(pass_data: dict, iso3Code: str = None) -> dict:
    """
    Parses GDP composition by sector of origin data including values, dates, and notes.

    Parameters:
        pass_data (dict): The dictionary containing GDP composition data by sector.

    Returns:
        dict: A dictionary with parsed GDP composition data by sector.
    """
    result = {}

    # Handle each GDP composition sector
    for key, mapped_key in KEY_MAPPING.items():
        data = pass_data.get(key, {})
        text = data.get("text", "")
        if text:
            # Skip NA values - these indicate no data available
            if text.upper().strip() == 'NA' or text.upper().startswith('NA '):
                result[mapped_key] = {
                    "value": None,
                    "unit": "%",
                    "year": None,
                    "note": "NA"
                }
                continue

            # Extract value and year
            # Handle both standard year format and fiscal year format (FY12/13)
            match = re.match(r"(-?[\d.]+)%\s+\((\d{4})", text)
            fy_match = re.match(r"(-?[\d.]+)%\s+\(FY(\d{2})/(\d{2})", text)
            if match:
                result[mapped_key] = {
                    "value": float(match.group(1)),
                    "unit": "%",
                    "year": int(match.group(2))
                }
            elif fy_match:
                # Convert FY12/13 to 2012 (use the first year of the fiscal year)
                fy_year = int(fy_match.group(2))
                full_year = 2000 + fy_year if fy_year < 50 else 1900 + fy_year
                result[mapped_key] = {
                    "value": float(fy_match.group(1)),
                    "unit": "%",
                    "year": full_year,
                    "fiscal_year": f"FY{fy_match.group(2)}/{fy_match.group(3)}"
                }
            else:
                logging.warning(f"Unexpected format in '{key}' data: {text}")

    # Handle 'note' field if it exists
    if "note" in pass_data:
        result["gdp_composition_note"] = clean_text(pass_data["note"])

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 19 >>> 'GDP - composition, by sector of origin'
    # --------------------------------------------------------------------------------------------------
    # "agriculture" - 'gdp_composition_agriculture'
    # "industry" - 'gdp_composition_industry'
    # "note" - 'gdp_composition_note'
    # "services" - 'gdp_composition_services'
    # --------------------------------------------------------------------------------------------------
    # ['gdp_composition_agriculture', 'gdp_composition_industry', 'gdp_composition_note', 'gdp_composition_services']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "agriculture": {
            "text": "0.9% (2017 est.)"
        },
        "industry": {
            "text": "19.1% (2017 est.)"
        },
        "services": {
            "text": "80% (2017 est.)"
        }
    }
    parsed_data = parse_gdp_composition_sector_of_origin(pass_data)
    print(parsed_data)
