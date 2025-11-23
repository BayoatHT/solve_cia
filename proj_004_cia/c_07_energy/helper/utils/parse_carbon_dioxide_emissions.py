import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_carbon_dioxide_emissions(carbon_data: dict) -> dict:
    """Parse carbon dioxide emissions from CIA Energy section."""
    result = {}
    if not carbon_data or not isinstance(carbon_data, dict):
        return result
    try:
        field_mappings = {
            'total emissions': 'carbon_total_emissions',
            'from coal and metallurgical coke': 'carbon_coal_metallurgical_coke',
            'from petroleum and other liquids': 'carbon_petroleum_other_liquids',
            'from consumed natural gas': 'carbon_consumed_natural_gas',
        }
        for cia_key, output_key in field_mappings.items():
            if cia_key in carbon_data:
                field_data = carbon_data[cia_key]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    if text and isinstance(text, str):
                        result[output_key] = clean_text(text)
        if 'note' in carbon_data:
            note_data = carbon_data['note']
            if isinstance(note_data, dict) and 'text' in note_data:
                note = note_data['text']
                if note and isinstance(note, str) and note.strip():
                    result['carbon_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['carbon_note'] = clean_text(note_data)
    except Exception as e:
        logging.error(f"Error parsing carbon_dioxide_emissions: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "from coal and metallurgical coke" - 'carbon_coal_metallurgical_coke'
    # "from consumed natural gas" - 'carbon_consumed_natural_gas'
    # "from petroleum and other liquids" - 'carbon_petroleum_other_liquids'
    # "note" - 'carbon_note'
    # "total emissions" - 'carbon_total_emissions'
    # --------------------------------------------------------------------------------------------------
    # ['carbon_coal_metallurgical_coke', 'carbon_consumed_natural_gas',
    # 'carbon_petroleum_other_liquids', 'carbon_note', 'carbon_total_emissions']
    # --------------------------------------------------------------------------------------------------
    carbon_data = {
        "total emissions": {
            "text": "4.941 billion metric tonnes of CO2 (2022 est.)"
        },
        "from coal and metallurgical coke": {
            "text": "938.649 million metric tonnes of CO2 (2022 est.)"
        },
        "from petroleum and other liquids": {
            "text": "2.26 billion metric tonnes of CO2 (2022 est.)"
        },
        "from consumed natural gas": {
            "text": "1.742 billion metric tonnes of CO2 (2022 est.)"
        },
        "note": {
            "text": ""
        }
    }
    parsed_data = parse_carbon_dioxide_emissions(carbon_data)
    print(parsed_data)
