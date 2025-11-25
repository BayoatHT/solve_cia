import re
import logging
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_natural_hazards(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse natural hazards data from CIA World Factbook for a given country.

    This parser extracts and structures natural hazard information including:
    - General hazards (applicable to entire country)
    - Region-specific hazards (e.g., metropolitan vs overseas territories)
    - Volcanism details

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'JPN', 'WLD')

    Returns:
        Dictionary with structured natural hazards data:
        {
            "general_hazards": ["tsunamis", "earthquakes", ...],
            "regions": {
                "region_name": ["hazard1", "hazard2", ...]
            },
            "volcanism": ["volcano details", ...]
        }

    Examples:
        >>> data = parse_natural_hazards('USA')
        >>> 'tsunamis' in data['general_hazards']
        True

        >>> data = parse_natural_hazards('JPN')
        >>> len(data.get('volcanism', [])) > 0
        True
    """
    result = {
        "general_hazards": [],
        "regions": {},
        "volcanism": []
    }

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Geography -> Natural hazards
    geography_section = raw_data.get('Geography', {})
    natural_hazards_data = geography_section.get('Natural hazards', {})

    if return_original:
        return natural_hazards_data


    if not natural_hazards_data or not isinstance(natural_hazards_data, dict):
        return result

    text = natural_hazards_data.get("text", "")
    if not text:
        return result

    # Split text by paragraphs
    paragraphs = re.split(r'</?p>', text)
    current_region = None

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        # Identify regional distinctions using <strong> tags
        region_match = re.match(r'<strong>(.*?):</strong>', paragraph)
        if region_match:
            current_region = region_match.group(
                1).strip().lower().replace(" ", "_")
            hazards = re.sub(
                r'<.*?>', '', paragraph[len(region_match.group(0)):]).strip()
            result["regions"][current_region] = [hazard.strip()
                                                 for hazard in hazards.split(';') if hazard.strip()]
        elif paragraph.startswith("<strong>volcanism:</strong>"):
            # Handle volcanism details
            volcanism_text = re.sub(r'<.*?>', '', paragraph).strip()
            volcanism_details = volcanism_text[len("volcanism:"):].strip()
            volcanism_entries = [
                entry.strip() for entry in volcanism_details.split(';') if entry.strip()]
            result["volcanism"].extend(volcanism_entries)
        else:
            # General hazards not related to specific regions
            general_hazards = re.sub(r'<.*?>', '', paragraph).strip()
            result["general_hazards"].extend(
                [hazard.strip() for hazard in general_hazards.split(';') if hazard.strip()])

    return result


if __name__ == "__main__":
    """Test parse_natural_hazards with real country data."""
    print("="*60)
    print("Testing parse_natural_hazards across countries")
    print("="*60)

    test_countries = ['USA', 'JPN', 'PHL', 'ISL', 'CHL', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_natural_hazards(iso3)

            if result['general_hazards']:
                hazards = result['general_hazards'][:3]
                print(f"  General hazards: {', '.join(hazards)}", end="")
                if len(result['general_hazards']) > 3:
                    print(f" ... and {len(result['general_hazards']) - 3} more")
                else:
                    print()

            if result['regions']:
                print(f"  Regional hazards: {list(result['regions'].keys())}")

            if result['volcanism']:
                print(f"  Volcanism: {len(result['volcanism'])} entries")
                # Show first entry summary
                first = result['volcanism'][0][:80] if result['volcanism'] else ""
                if first:
                    print(f"    {first}...")

            if not any([result['general_hazards'], result['regions'], result['volcanism']]):
                print("  No hazards found")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
