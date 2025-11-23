import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_gini(pass_data: dict, iso3Code: str = None) -> dict:
    """
    Parses Gini Index data, including values, years, and notes if available.

    Parameters:
        pass_data (dict): The dictionary containing Gini Index data.

    Returns:
        dict: A dictionary with parsed Gini Index data.
    """
    result = {}

    # Parse each Gini Index entry
    for key, data in pass_data.items():
        if key.startswith("Gini Index"):
            text = data.get("text", "")
            # Match the Gini value and year if present
            match = re.match(r"([\d.]+)\s*\((\d{4})", text)
            if match:
                year_key = f"gini_index_{match.group(2)}"
                result[year_key] = {
                    "value": float(match.group(1)),
                    "year": int(match.group(2))
                }
            else:
                logging.warning(f"Unexpected format in '{key}' data: {text}")

    # Handle 'note' field if it exists
    if "note" in pass_data:
        result["gini_note"] = clean_text(pass_data["note"])

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 22 >>> 'Gini Index coefficient - distribution of family income'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Gini Index coefficient - distribution of family income 2021": {
            "text": "39.8 (2021 est.)"
        },
        "note": "<b>note:</b> index (0-100) of income distribution; higher values represent greater inequality"
    }
    parsed_data = parse_gini(pass_data)
    print(parsed_data)
