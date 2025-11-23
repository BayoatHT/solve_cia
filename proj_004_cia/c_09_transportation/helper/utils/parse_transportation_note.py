"""
Parse transportation note from CIA World Factbook.
"""
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_transportation_note(transportation_note_data: dict, iso3Code: str = None) -> dict:
    """
    Parse transportation note.

    Args:
        transportation_note_data: Dict with 'text' containing the note
        iso3Code: Country ISO3 code

    Returns:
        Dict with:
            - transportation_note: str (the note text)

    Example:
        Input: {"text": "the new airport on Saint Helena opened for limited operations..."}
        Output: {'transportation_note': 'the new airport on Saint Helena opened for limited operations...'}
    """
    result = {}

    if not transportation_note_data:
        return result

    try:
        if 'text' in transportation_note_data:
            text = transportation_note_data['text']
            if text and isinstance(text, str) and text.strip():
                result['transportation_note'] = clean_text(text)

    except Exception as e:
        logging.error(f"Error parsing transportation_note for {iso3Code}: {e}")

    return result


# Example usage
if __name__ == "__main__":
    test_data = {"text": "the new airport on Saint Helena opened for limited operations in July 2016"}
    parsed = parse_transportation_note(test_data, "SHN")
    print(parsed)
