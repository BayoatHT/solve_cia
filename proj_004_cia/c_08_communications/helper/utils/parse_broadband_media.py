import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_broadband_media(broadband_media_data: dict) -> dict:
    """Parse broadcast media from CIA Communications section."""
    result = {}
    if not broadband_media_data or not isinstance(broadband_media_data, dict):
        return result
    try:
        if 'text' in broadband_media_data:
            text = broadband_media_data['text']
            if text and isinstance(text, str):
                result['broadcast_media'] = clean_text(text)
    except Exception as e:
        logging.error(f"Error parsing broadband_media: {e}")
    return result


# Example usage
if __name__ == "__main__":
    broadband_media_data = {
        "text": "4 major terrestrial TV networks with affiliate stations throughout the country, plus cable and satellite networks, independent stations, and a limited public broadcasting sector that is largely supported by private grants; overall, thousands of TV stations broadcasting; multiple national radio networks with many affiliate stations; while most stations are commercial, National Public Radio (NPR) has a network of some 900 member stations; satellite radio available; in total, over 15,000 radio stations operating (2018)"
    }
    parsed_data = parse_broadband_media(broadband_media_data)
    print(parsed_data)
