import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_marine_fisheries(fisheries_data: dict, iso3Code: str = None) -> dict:
    """
    Parse marine fisheries data (primarily for ocean entities).

    Args:
        fisheries_data: Dictionary with marine fisheries information
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured marine fisheries data
    """
    result = {
        "marine_fisheries": {
            "description": None,
            "total_catch_mt": None,
            "year": None,
            "regional_bodies": None,
            "major_producers": [],
            "principal_catches": []
        },
        "marine_fisheries_note": ""
    }

    if not fisheries_data or not isinstance(fisheries_data, dict):
        return result

    text = fisheries_data.get('text', '')
    if text and text.upper() != 'NA':
        cleaned = clean_text(text)
        result['marine_fisheries']['description'] = cleaned

        # Try to extract total catch
        catch_match = re.search(r'total catch of ([\d,]+)\s*mt', cleaned, re.IGNORECASE)
        if catch_match:
            result['marine_fisheries']['total_catch_mt'] = int(catch_match.group(1).replace(',', ''))

        # Try to extract year
        year_match = re.search(r'in (\d{4})', cleaned)
        if year_match:
            result['marine_fisheries']['year'] = year_match.group(1)

        # Try to extract regional fisheries bodies
        bodies_match = re.search(r'Regional fisheries bodies:\s*(.+?)(?:\.|$)', cleaned, re.IGNORECASE)
        if bodies_match:
            result['marine_fisheries']['regional_bodies'] = bodies_match.group(1).strip()

        # Try to extract major producers with catch amounts
        producer_pattern = re.compile(r'([A-Za-z\s]+)\s*\(([\d,]+)\s*mt\)', re.IGNORECASE)
        producers = producer_pattern.findall(cleaned)
        for name, catch in producers[:10]:  # Limit to first 10
            name = name.strip()
            if name and len(name) > 2:
                result['marine_fisheries']['major_producers'].append({
                    'country': name,
                    'catch_mt': int(catch.replace(',', ''))
                })

    return result


if __name__ == "__main__":
    test_data = {
        "text": "the Southern Ocean fishery has a total catch of 388,901 mt in 2021; Norway (241,408 mt), China (47,605 mt). Regional fisheries bodies: Commission for the Conservation of Antarctic Marine Living Resources"
    }
    print(parse_marine_fisheries(test_data))
