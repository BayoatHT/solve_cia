import re
import logging

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_natural_hazards(natural_hazards_data: dict, iso3Code: str=None) -> dict:
    """
    Parses the 'Natural hazards' data for a country, considering regional distinctions and volcanism.

    Parameters:
        natural_hazards_data (dict): The 'Natural hazards' section from the data.

    Returns:
        dict: A dictionary containing parsed details of natural hazards, categorized by region and type.
    """
    result = {
        "general_hazards": [],
        "regions": {},
        "volcanism": []
    }

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


# Example usage
if __name__ == "__main__":
    natural_hazards_data = {
        "text": "<p>tsunamis; volcanoes; earthquake activity around Pacific Basin; hurricanes along the Atlantic and Gulf of Mexico coasts; tornadoes in the Midwest and Southeast; mud slides in California; forest fires in the west; flooding; permafrost in northern Alaska, a major impediment to development</p> <p><strong>volcanism:</strong> volcanic activity in the Hawaiian Islands, Western Alaska, the Pacific Northwest, and in the Northern Mariana Islands; both Mauna Loa (4,170 m) in Hawaii and Mount Rainier (4,392 m) in Washington have been deemed Decade Volcanoes by the International Association of Volcanology and Chemistry of the Earth's Interior, worthy of study due to their explosive history and close proximity to human populations; Pavlof (2,519 m) is the most active volcano in Alaska's Aleutian Arc and poses a significant threat to air travel since the area constitutes a major flight path between North America and East Asia; St. Helens (2,549 m), famous for the devastating 1980 eruption, remains active today; numerous other historically active volcanoes exist, mostly concentrated in the Aleutian arc and Hawaii; they include: in Alaska: Aniakchak, Augustine, Chiginagak, Fourpeaked, Iliamna, Katmai, Kupreanof, Martin, Novarupta, Redoubt, Spurr, Wrangell, Trident, Ugashik-Peulik, Ukinrek Maars, Veniaminof; in Hawaii: Haleakala, Kilauea, Loihi; in the Northern Mariana Islands: Anatahan; and in the Pacific Northwest: Mount Baker, Mount Hood; see note 2 under \"Geography - note\"</p>"
    }
    parsed_data = parse_natural_hazards(natural_hazards_data)
    print(parsed_data)
