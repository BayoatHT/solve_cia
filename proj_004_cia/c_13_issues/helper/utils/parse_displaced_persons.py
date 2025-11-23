import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_displaced_persons(displaced_data: dict, iso3Code: str = None) -> dict:
    """
    Parses data related to displaced persons, including refugees, stateless persons, and internally displaced persons (IDPs).

    Parameters:
        displaced_data (dict): The dictionary containing displaced persons data.

    Returns:
        dict: A dictionary containing parsed information for refugees, stateless persons, and IDPs.

    Output keys with value extraction pattern:
        - refugees_description: str (full refugee text)
        - refugees_total_value: int (total refugees admitted if available)
        - refugees_total_year: int (year of refugee data)
        - refugees_by_origin: list of {country, count} dicts
        - stateless_persons_value: int (number of stateless persons)
        - stateless_persons_year: int (year of stateless data)
        - idp_value: int (number of internally displaced persons)
        - idp_year: int (year of IDP data)
        - idp_description: str (full IDP text)
    """
    result = {}

    # Handle 'refugees (country of origin)'
    refugees_text = displaced_data.get(
        "refugees (country of origin)", {}).get("text", "")
    if refugees_text:
        cleaned = clean_text(refugees_text)
        result["refugees_description"] = cleaned

        # Try to extract total refugee number: "admitted 25,465 refugees"
        total_match = re.search(r'admitted\s+([\d,]+)\s+refugees', refugees_text)
        if total_match:
            result["refugees_total_value"] = int(total_match.group(1).replace(',', ''))

        # Extract year: "FY2022" or "(2022)"
        year_match = re.search(r'FY(\d{4})|[(\s](\d{4})[)\s,]', refugees_text)
        if year_match:
            result["refugees_total_year"] = int(year_match.group(1) or year_match.group(2))

        # Extract refugees by origin: "7,810 (Democratic Republic of the Congo)"
        # Pattern matches: number (country name) - requires at least one digit
        origin_pattern = re.compile(r'(\d[\d,]*)\s*\(([^)]+)\)')
        origins = []
        for match in origin_pattern.finditer(refugees_text):
            count_str = match.group(1).replace(',', '')
            country = match.group(2).strip()
            # Skip if count is empty or country is just a year/date reference
            if not count_str or country.isdigit() or len(country) <= 4:
                continue
            # Skip date references like "mid-year 2022"
            if 'year' in country.lower() or 'as of' in country.lower():
                continue
            try:
                count = int(count_str)
                origins.append({
                    "country": country,
                    "count": count
                })
            except ValueError:
                continue

        if origins:
            result["refugees_by_origin"] = origins

    # Handle 'stateless persons'
    stateless_text = displaced_data.get(
        "stateless persons", {}).get("text", "")
    if stateless_text:
        # Match patterns like "47 (2022)" or "1,234 (2022)"
        match = re.match(r"([\d,]+)\s*\((\d{4})\)?", stateless_text)
        if match:
            result["stateless_persons_value"] = int(match.group(1).replace(',', ''))
            result["stateless_persons_year"] = int(match.group(2))
        else:
            # Try just number
            num_match = re.match(r"([\d,]+)", stateless_text)
            if num_match:
                result["stateless_persons_value"] = int(num_match.group(1).replace(',', ''))

    # Handle 'IDPs'
    idp_text = displaced_data.get("IDPs", {}).get("text", "")
    if idp_text:
        cleaned_idp = clean_text(idp_text)
        result["idp_description"] = cleaned_idp

        # Extract the main numeric value: "6.38 million" or "30,000" or "approximately 2 million"
        # Pattern handles: 6.38 million, 30,000, approximately 2 million, 1.5 million
        main_pattern = re.compile(
            r'(?:approximately\s+)?([\d,]+(?:\.\d+)?)\s*(million|thousand)?',
            re.IGNORECASE
        )

        main_match = main_pattern.search(idp_text)
        if main_match:
            number_str = main_match.group(1).replace(',', '')
            number = float(number_str)
            magnitude = main_match.group(2)
            if magnitude:
                if magnitude.lower() == "million":
                    number *= 1_000_000
                elif magnitude.lower() == "thousand":
                    number *= 1_000
            result["idp_value"] = int(number)

        # Extract year: "(2023)" at end typically
        year_match = re.search(r'\((\d{4})\)\s*$', idp_text)
        if year_match:
            result["idp_year"] = int(year_match.group(1))

    return result


# Example usage
if __name__ == "__main__":
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data
    from pprint import pprint

    # Test with USA
    print("=== USA Displaced Persons ===")
    data = load_country_data('USA')
    displaced = data.get('Transnational Issues', {}).get('Refugees and internally displaced persons', {})
    parsed = parse_displaced_persons(displaced, 'USA')
    pprint(parsed)

    # Test with Syria (has IDPs)
    print("\n=== Syria Displaced Persons ===")
    data = load_country_data('SYR')
    displaced = data.get('Transnational Issues', {}).get('Refugees and internally displaced persons', {})
    parsed = parse_displaced_persons(displaced, 'SYR')
    pprint(parsed)

    # Test with Germany
    print("\n=== Germany Displaced Persons ===")
    data = load_country_data('DEU')
    displaced = data.get('Transnational Issues', {}).get('Refugees and internally displaced persons', {})
    parsed = parse_displaced_persons(displaced, 'DEU')
    pprint(parsed)
