import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_illicit_drugs(drugs_data: dict, iso3Code: str = None) -> dict:
    """
    Parses data related to illicit drugs.

    Parameters:
        drugs_data (dict): The dictionary containing illicit drug information.

    Returns:
        dict: A dictionary containing parsed illicit drug information.

    Output keys:
        - illicit_drugs_description: str (full description text)
        - is_producer: bool (if country produces drugs)
        - is_consumer: bool (if country consumes drugs)
        - is_transit: bool (if country is a transit point)
        - drugs_mentioned: list (specific drugs mentioned)
    """
    result = {}

    drugs_text = drugs_data.get("text", "")
    if not drugs_text:
        return result

    # Clean HTML and normalize text
    cleaned_text = clean_text(drugs_text)

    if cleaned_text:
        result["illicit_drugs_description"] = cleaned_text

        # Identify if producer, consumer, or transit
        text_lower = cleaned_text.lower()

        result["is_producer"] = any(term in text_lower for term in [
            'producer', 'produces', 'production', 'cultivat', 'manufactur', 'illicit producer'
        ])

        result["is_consumer"] = any(term in text_lower for term in [
            'consumer', 'consumption', 'domestic use', 'major market'
        ])

        result["is_transit"] = any(term in text_lower for term in [
            'transit', 'transshipment', 'trafficking', 'smuggling route'
        ])

        result["is_money_laundering"] = 'money-laundering' in text_lower or 'money laundering' in text_lower

        # Extract specific drugs mentioned
        drug_names = [
            'cocaine', 'heroin', 'marijuana', 'cannabis', 'methamphetamine',
            'ecstasy', 'opium', 'fentanyl', 'amphetamines', 'hashish',
            'depressants', 'stimulants', 'hallucinogens', 'ketamine',
            'synthetic drugs', 'precursor chemicals'
        ]

        drugs_found = []
        for drug in drug_names:
            if drug in text_lower:
                drugs_found.append(drug)

        if drugs_found:
            result["drugs_mentioned"] = drugs_found

    return result


# Example usage
if __name__ == "__main__":
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data
    from pprint import pprint

    # Test with USA
    data = load_country_data('USA')
    drugs_data = data.get('Transnational Issues', {}).get('Illicit drugs', {})
    parsed = parse_illicit_drugs(drugs_data, 'USA')
    print("=== USA Illicit Drugs ===")
    pprint(parsed)

    # Test with Colombia
    data = load_country_data('COL')
    drugs_data = data.get('Transnational Issues', {}).get('Illicit drugs', {})
    parsed = parse_illicit_drugs(drugs_data, 'COL')
    print("\n=== Colombia Illicit Drugs ===")
    pprint(parsed)
