import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_military_expenditures(iso3Code: str) -> dict:
    """
    Parse military expenditures data from CIA Military and Security section.

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN')

    Returns:
        dict: A dictionary with structured information for military expenditures over the years.
    """
    result = {}

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    military_section = raw_data.get('Military and Security', {})
    military_expenditures_data = military_section.get('Military expenditures', {})

    if not military_expenditures_data or not isinstance(military_expenditures_data, dict):
        return result

    try:
        # Handle note
        if military_expenditures_data.get("note"):
            result["military_note"] = clean_text(military_expenditures_data.get("note", ""))

        # Updated regex pattern to extract the value, unit, and date
        expenditure_pattern = re.compile(
            r"([\d\.]+)% of GDP \((\d{4})\s*(?:est\.)?\)")

        # Loop through each key, looking for military expenditure entries by year
        for key, data in military_expenditures_data.items():
            # Skip the 'note' key as it's already processed
            if key == "note":
                continue

            # Skip if not a dict
            if not isinstance(data, dict):
                continue

            # Extract the year from the key (last 4 characters)
            year = key[-4:]
            expenditure_key = f"military_expenditure_{year}"

            # Initialize a dictionary structure for this expenditure
            result[expenditure_key] = {
                "value": 0,
                "unit": "%",
                "date": year
            }

            # Extract the text and parse value and date if present
            text = data.get("text", "")
            if not text:
                logger.warning(f"No data found in {key}")
                continue

            match = expenditure_pattern.match(text)
            if match:
                result[expenditure_key]["value"] = float(match.group(1))
                result[expenditure_key]["date"] = match.group(2)
            else:
                logger.warning(f"Data format unrecognized in {key}")

    except Exception as e:
        logger.error(f"Error parsing military expenditures for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Testing parse_military_expenditures")
    print("=" * 60)
    for iso3 in ['USA', 'CHN', 'RUS', 'IND', 'DEU', 'GBR']:
        print(f"\n{iso3}:")
        try:
            result = parse_military_expenditures(iso3)
            if result:
                # Find expenditure keys
                exp_keys = [k for k in result.keys() if k.startswith('military_expenditure_')]
                if exp_keys:
                    exp_keys.sort(reverse=True)
                    for key in exp_keys[:3]:
                        data = result[key]
                        print(f"  {data['date']}: {data['value']}% of GDP")
                else:
                    print("  No expenditure data found")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "=" * 60)
    print("✓ Tests complete")
