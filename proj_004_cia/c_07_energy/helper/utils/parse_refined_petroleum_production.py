import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_refined_petroleum_production(pass_data: dict) -> dict:
    """Parse refined petroleum production from CIA Energy section."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['refined_petroleum_production'] = clean_text(text)
    except Exception as e:
        logging.error(f"Error parsing refined_petroleum_production: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'refined_petroleum_production'
    # --------------------------------------------------------------------------------------------------
    # ['refined_petroleum_production']
    # --------------------------------------------------------------------------------------------------
    pass_data = {

    }
    parsed_data = parse_refined_petroleum_production(pass_data)
    print(parsed_data)
