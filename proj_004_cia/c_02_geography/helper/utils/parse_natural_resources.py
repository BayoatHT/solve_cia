######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import re
import logging

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# ---------------------------------------------------------------------------------------------------------------------


def parse_natural_resources(natural_resources_data: dict, iso3Code: str = None, return_original: bool = False) -> dict:
    """
    Parse natural resources data from CIA World Factbook for a given country.

    This parser extracts and structures natural resource information including:
    - Main resource lists
    - Territory-specific resources (e.g., metropolitan vs overseas)
    - Resource notes and additional context

    Args:
        natural_resources_data: The 'Natural resources' section from the Geography data
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'FRA', 'WLD')
        return_original: If True, return the raw data without parsing

    Returns:
        Dictionary with structured natural resources data:
        {
            "natural_resources": {
                "main": ["coal", "iron ore", ...],  # or
                "metropolitan_france": ["coal", ...],
                "french_guiana": ["gold", ...]
            },
            "natural_resources_note": str
        }

    Examples:
        >>> data = parse_natural_resources({'text': 'coal, iron ore'}, 'USA')
        >>> 'coal' in data['natural_resources'].get('main', [])
        True
    """
    result = {
        "natural_resources": {},
        "natural_resources_note": ""
    }

    if return_original:
        return natural_resources_data

    if not natural_resources_data or not isinstance(natural_resources_data, dict):
        return result

    # Extract the text content for natural resources
    text = natural_resources_data.get('text', '')
    if text:
        # Check if the text contains <em> tags, indicating territories
        if '<em>' in text:
            # Split the text by ';' to separate different regions
            regions = text.split(';')
            for region in regions:
                region = region.strip()
                if not region:
                    continue
                # Split each region by <em> tags
                parts = re.split(r'<em>|</em>', region)
                current_key = None
                for part in parts:
                    part = part.strip()
                    if not part:
                        continue
                    if ':' in part:
                        # This is a region name (e.g., "metropolitan France:")
                        current_key = part.replace(
                            ':', '').strip().replace(' ', '_').lower()
                        result["natural_resources"][current_key] = []
                    else:
                        # This is the list of resources for the current region
                        resources = [resource.strip()
                                     for resource in part.split(',')]
                        if current_key:
                            result["natural_resources"][current_key].extend(
                                resources)
        else:
            # If no <em> tags, treat as a simple list of natural resources
            resources = [resource.strip() for resource in text.split(',')]
            result["natural_resources"]["main"] = resources

    # Extract the note content for natural resources if present
    note = natural_resources_data.get('note', '')
    if note:
        # Clean the note text by removing the <strong> tags and HTML
        note_cleaned = re.sub(r'<strong>|</strong>', '', note).strip()
        note_cleaned = re.sub(r'^note\s*\d*:\s*', '', note_cleaned, flags=re.IGNORECASE)
        result["natural_resources_note"] = note_cleaned

    return result


if __name__ == "__main__":
    """Test parse_natural_resources with real country data."""
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

    print("="*60)
    print("Testing parse_natural_resources across countries")
    print("="*60)

    test_countries = ['USA', 'FRA', 'CHN', 'BRA', 'SAU', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            raw_data = load_country_data(iso3)
            natural_resources_data = raw_data.get('Geography', {}).get('Natural resources', {})
            result = parse_natural_resources(natural_resources_data, iso3)
            resources = result['natural_resources']

            if resources:
                print(f"  Resource categories: {list(resources.keys())}")

                # Show resources for each category
                for category, resource_list in resources.items():
                    if resource_list:
                        display_resources = resource_list[:5]
                        print(f"    {category}: {', '.join(display_resources)}", end="")
                        if len(resource_list) > 5:
                            print(f" ... and {len(resource_list) - 5} more")
                        else:
                            print()
            else:
                print("  No resources found")

            if result.get('natural_resources_note'):
                note = result['natural_resources_note'][:70]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
