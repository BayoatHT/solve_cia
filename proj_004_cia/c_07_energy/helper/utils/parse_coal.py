import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_coal(coal_data: dict) -> dict:
    """Parse coal data from CIA Energy section."""
    result = {}
    if not coal_data or not isinstance(coal_data, dict):
        return result
    try:
        field_mappings = {
            'production': 'coal_production',
            'consumption': 'coal_consumption',
            'exports': 'coal_exports',
            'imports': 'coal_imports',
            'proven reserves': 'coal_proven_reserves',
        }
        for cia_key, output_key in field_mappings.items():
            if cia_key in coal_data:
                field_data = coal_data[cia_key]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    if text and isinstance(text, str):
                        result[output_key] = clean_text(text)
        if 'note' in coal_data:
            note_data = coal_data['note']
            if isinstance(note_data, dict) and 'text' in note_data:
                note = note_data['text']
                if note and isinstance(note, str) and note.strip():
                    result['coal_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['coal_note'] = clean_text(note_data)
    except Exception as e:
        logging.error(f"Error parsing coal: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "consumption" - 'coal_consumption'
    # "exports" - 'coal_exports'
    # "imports" - 'coal_imports'
    # "note" - 'coal_note'
    # "production"- 'coal_production'
    # "proven reserves" - 'coal_proven_reserves'
    # --------------------------------------------------------------------------------------------------
    # ['coal_consumption', 'coal_exports', 'coal_imports', 'coal_note',
    # 'coal_production', 'coal_proven_reserves']
    # --------------------------------------------------------------------------------------------------
    coal_data = {
        "production": {
            "text": "548.849 million metric tons (2022 est.)"
        },
        "consumption": {
            "text": "476.044 million metric tons (2022 est.)"
        },
        "exports": {
            "text": "80.081 million metric tons (2022 est.)"
        },
        "imports": {
            "text": "5.788 million metric tons (2022 est.)"
        },
        "proven reserves": {
            "text": "248.941 billion metric tons (2022 est.)"
        },
        "note": {
            "text": ""
        }
    }
    parsed_data = parse_coal(coal_data)
    print(parsed_data)
