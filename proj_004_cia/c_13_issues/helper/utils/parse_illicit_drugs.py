import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_illicit_drugs(iso3Code: str) -> dict:
    """
    Parse illicit drugs data from CIA Transnational Issues section for a given country.

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'COL')

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

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    issues_section = raw_data.get('Transnational Issues', {})
    drugs_data = issues_section.get('Illicit drugs', {})

    if not drugs_data or not isinstance(drugs_data, dict):
        return result

    try:
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

    except Exception as e:
        logger.error(f"Error parsing illicit drugs for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Testing parse_illicit_drugs")
    print("=" * 60)
    for iso3 in ['USA', 'COL', 'MEX', 'AFG', 'NLD', 'THA']:
        print(f"\n{iso3}:")
        try:
            result = parse_illicit_drugs(iso3)
            if result.get('illicit_drugs_description'):
                desc = result['illicit_drugs_description'][:60]
                print(f"  Description: {desc}...")
                flags = []
                if result.get('is_producer'):
                    flags.append('producer')
                if result.get('is_transit'):
                    flags.append('transit')
                if result.get('is_consumer'):
                    flags.append('consumer')
                if flags:
                    print(f"  Flags: {', '.join(flags)}")
                if result.get('drugs_mentioned'):
                    print(f"  Drugs: {', '.join(result['drugs_mentioned'][:5])}")
            else:
                print("  No illicit drugs data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "=" * 60)
    print("✓ Tests complete")
