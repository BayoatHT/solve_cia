######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import re
import logging

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
# ---------------------------------------------------------------------------------------------------------------------


def parse_natural_resources(natural_resources_data: dict, iso3Code: str=None) -> dict:
    """
    Parses the 'Natural resources' data for specific countries.

    Parameters:
        natural_resources_data (dict): The 'Natural resources' section from the data.

    Returns:
        dict: A dictionary containing parsed natural resources details, organized as an array of natural resources
              and any accompanying notes.
    """
    result = {
        "natural_resources": {},
        "natural_resources_note": ""
    }

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
        # Clean the note text by removing the <strong> tags
        note_cleaned = re.sub(r'<strong>|</strong>', '', note).strip()
        result["natural_resources_note"] = note_cleaned

    return result


# Example usage
if __name__ == "__main__":
    natural_resources_data = {
        "text": "<em>metropolitan France:</em> coal, iron ore, bauxite, zinc, uranium, antimony, arsenic, potash, feldspar, fluorspar, gypsum, timber, arable land, fish; <em>French Guiana:</em> gold deposits, petroleum, kaolin, niobium, tantalum, clay",
        "note": "<strong>note: </strong>the US has the world's largest coal reserves with 491 billion short tons accounting for 27% of the world's total"
    }
    print(parse_natural_resources(natural_resources_data))
