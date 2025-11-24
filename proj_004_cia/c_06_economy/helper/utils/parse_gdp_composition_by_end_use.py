import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Key mapping dictionary for clear output structure
KEY_MAPPING = {
    "exports of goods and services": "gdp_exports",
    "government consumption": "gdp_govt_consumption",
    "household consumption": "gdp_household_consumption",
    "imports of goods and services": "gdp_imports",
    "investment in fixed capital": "gdp_investment_fixed_capital",
    "investment in inventories": "gdp_investment_inventories"
}


def parse_gdp_composition_by_end_use(pass_data: dict, iso3Code: str = None) -> dict:
    """
    Parses GDP composition by end use data including values, dates, and notes.

    Parameters:
        pass_data (dict): The dictionary containing GDP composition data.

    Returns:
        dict: A dictionary with parsed GDP composition data by end use.
    """
    result = {}

    # Handle each GDP composition category
    for key, mapped_key in KEY_MAPPING.items():
        data = pass_data.get(key, {})
        text = data.get("text", "")
        if text:
            # Skip NA values - these indicate no data available
            # Handles "NA", "NA (2007 est.)", and "(2016 est.) NA"
            if 'NA' in text.upper():
                # Try to extract year if present
                year_match = re.search(r'\((\d{4})', text)
                result[mapped_key] = {
                    "value": None,
                    "unit": "%",
                    "year": int(year_match.group(1)) if year_match else None,
                    "note": "NA"
                }
                continue

            # Extract value and year
            value_match = re.match(r"(-?[\d.]+)%\s+\((\d{4})", text)
            if value_match:
                result[mapped_key] = {
                    "value": float(value_match.group(1)),
                    "unit": "%",
                    "year": int(value_match.group(2))
                }
            else:
                logging.warning(f"Unexpected format in '{key}' data: {text}")

    # Handle 'note' field if it exists
    if "note" in pass_data:
        result["gdp_composition_note"] = clean_text(pass_data["note"])

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 18 >>> 'GDP - composition, by end use'
    # --------------------------------------------------------------------------------------------------
    # "exports of goods and services" - 'gdp_composition_exports'
    # "government consumption" - 'gdp_composition_govt_consumption'
    # "household consumption" - 'gdp_composition_household_consumption'
    # "imports of goods and services" - 'gdp_composition_imports'
    # "investment in fixed capital" - 'gdp_composition_investment_fixed_capital'
    # "investment in inventories" - 'gdp_composition_investment_inventories'
    # "note" - 'gdp_composition_note'
    # --------------------------------------------------------------------------------------------------
    # ['gdp_composition_exports', 'gdp_composition_govt_consumption', 'gdp_composition_household_consumption',
    # 'gdp_composition_imports', 'gdp_composition_investment_fixed_capital', 'gdp_composition_investment_inventories',
    # 'gdp_composition_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "household consumption": {
            "text": "68.4% (2017 est.)"
        },
        "government consumption": {
            "text": "17.3% (2017 est.)"
        },
        "investment in fixed capital": {
            "text": "17.2% (2017 est.)"
        },
        "investment in inventories": {
            "text": "0.1% (2017 est.)"
        },
        "exports of goods and services": {
            "text": "12.1% (2017 est.)"
        },
        "imports of goods and services": {
            "text": "-15% (2017 est.)"
        }
    }
    parsed_data = parse_gdp_composition_by_end_use(pass_data)
    print(parsed_data)
