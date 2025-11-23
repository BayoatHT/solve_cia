import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_population_below_poverty(pass_data: dict, iso3Code: str = None) -> dict:
    """Parse population below poverty from CIA Economy section."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['population_below_poverty'] = clean_text(text)
        if 'note' in pass_data:
            note = pass_data['note']
            if isinstance(note, str) and note.strip():
                result['population_below_poverty_note'] = clean_text(note)
    except Exception as e:
        logging.error(f"Error parsing population_below_poverty: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 32 >>> 'Population below poverty line'
    # --------------------------------------------------------------------------------------------------
    # "note" -  'population_below_poverty_line_note'
    # "text" - 'population_below_poverty_line'
    # --------------------------------------------------------------------------------------------------
    # ['population_below_poverty_line', 'population_below_poverty_line_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "16.1% (2015 est.)",
        "note": "<b>note:</b> % of population with income below national poverty line"
    }
    parsed_data = parse_population_below_poverty(pass_data)
    print(parsed_data)
