import re
import logging

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_maritime_claims(maritime_claims_data: dict, iso3Code: str = None) -> dict:
    """
    Parses the 'Maritime claims' data for a country.

    Parameters:
        maritime_claims_data (dict): The 'Maritime claims' section from the data.
        iso3Code (str): The ISO3 code of the country (optional).

    Returns:
        dict: A dictionary containing parsed details of maritime claims.
    """
    # Check for cases like "none (landlocked)"
    if "text" in maritime_claims_data:
        status_text = maritime_claims_data["text"].strip().lower()
        if status_text == "none (landlocked)" or "none" in status_text:
            return {"status": maritime_claims_data["text"]}

    # Continue parsing if no "status" text is found
    result = {}
    for key, value in maritime_claims_data.items():
        text = value.get("text", "")
        if not text:
            result[key] = {"value": 0, "unit": "", "note": ""}
            continue

        # Handle "not specified" case
        if "not specified" in text.lower():
            result[key] = {"value": 0, "unit": "", "note": ""}
            continue

        # Extract note if present in parentheses
        note_match = re.search(r"\(([^)]+)\)", text)
        note = note_match.group(1).strip() if note_match else ""

        # Remove note from text
        cleaned_text = re.sub(r"\(.*?\)", "", text).strip()

        # Extract numeric value and unit
        match = re.match(r"([\d,\.]+)\s*(\w+)", cleaned_text)
        if match:
            value = float(match.group(1).replace(",", ""))
            unit = match.group(2)
            result[key] = {"value": value, "unit": unit, "note": note}
        else:
            result[key] = {"value": 0, "unit": "", "note": note}

    return result


def parse_wld_maritime_claims(maritime_claims_data: dict) -> dict:
    """
    Parses the 'Maritime claims' data for a country.

    Parameters:
        maritime_claims_data (dict): The 'Maritime claims' section from the data.

    Returns:
        dict: A dictionary containing parsed details of maritime claims.
    """
    result = {
        "general_claims": [],
        "additional_zones": [],
        "boundary_situations": ""
    }

    text = maritime_claims_data.get("text", "")
    if not text:
        return result

    # Check for cases like "none (landlocked)"
    status_text = text.strip().lower()
    if status_text == "none (landlocked)" or "none" in status_text:
        return {"status": text}

    # Remove HTML tags and extra spaces
    cleaned_text = re.sub(r"<.*?>", "", text).strip()

    # Split the claims text into parts by semicolons
    parts = [part.strip() for part in cleaned_text.split(';')]

    for part in parts:
        if "territorial sea" in part or "contiguous zone" in part or "exclusive economic zone" in part:
            result["general_claims"].append(part)
        elif "additional zones" in part or "continental shelf" in part or "exclusive fishing zone" in part:
            result["additional_zones"].append(part)
        elif "boundary situations" in part:
            result["boundary_situations"] = part

    return result


# Example usage
if __name__ == "__main__":
    maritime_claims_data = {
        "territorial sea": {
            "text": "12 nm"
        },
        "contiguous zone": {
            "text": "24 nm"
        },
        "exclusive economic zone": {
            "text": "200 nm (estimated)"
        },
        "continental shelf": {
            "text": "not specified"
        }
    }
    parsed_data = parse_maritime_claims(maritime_claims_data)
    print(parsed_data)

    # Example for landlocked country
    landlocked_data = {
        "text": "none (landlocked)"
    }
    parsed_landlocked_data = parse_maritime_claims(landlocked_data)
    print(parsed_landlocked_data)
