import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_electricity_sources(electricity_sources_data: dict) -> dict:
    """Parse electricity generation sources from CIA Energy section."""
    result = {}
    if not electricity_sources_data or not isinstance(electricity_sources_data, dict):
        return result
    try:
        field_mappings = {
            'fossil fuels': 'electricity_generation_fossil_fuels',
            'nuclear': 'electricity_generation_nuclear',
            'solar': 'electricity_generation_solar',
            'wind': 'electricity_generation_wind',
            'hydroelectricity': 'electricity_generation_hydroelectricity',
            'geothermal': 'electricity_generation_geothermal',
            'biomass and waste': 'electricity_generation_biomass_waste',
            'tide and wave': 'electricity_generation_tide_wave',
        }
        for cia_key, output_key in field_mappings.items():
            if cia_key in electricity_sources_data:
                field_data = electricity_sources_data[cia_key]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    if text and isinstance(text, str):
                        result[output_key] = clean_text(text)
        if 'note' in electricity_sources_data:
            note_data = electricity_sources_data['note']
            if isinstance(note_data, dict) and 'text' in note_data:
                note = note_data['text']
                if note and isinstance(note, str) and note.strip():
                    result['electricity_generation_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['electricity_generation_note'] = clean_text(note_data)
    except Exception as e:
        logging.error(f"Error parsing electricity_sources: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "biomass and waste" - 'electricity_generation_biomass_waste'
    # "fossil fuels" - 'electricity_generation_fossil_fuels'
    # "geothermal" - 'electricity_generation_geothermal'
    # "hydroelectricity" - 'electricity_generation_hydroelectricity'
    # "note" - 'electricity_generation_note'
    # "nuclear" - 'electricity_generation_nuclear'
    # "solar" - 'electricity_generation_solar'
    # "tide and wave" - 'electricity_generation_tide_wave'
    # "wind" - 'electricity_generation_wind'
    # --------------------------------------------------------------------------------------------------
    # ['electricity_generation_biomass_waste', 'electricity_generation_fossil_fuels',
    # 'electricity_generation_geothermal', 'electricity_generation_hydroelectricity',
    # 'electricity_generation_note', 'electricity_generation_nuclear', 'electricity_generation_solar',
    # 'electricity_generation_tide_wave', 'electricity_generation_wind']
    # --------------------------------------------------------------------------------------------------
    electricity_sources_data = {
        "fossil fuels": {
            "text": "59.5% of total installed capacity (2022 est.)"
        },
        "nuclear": {
            "text": "18% of total installed capacity (2022 est.)"
        },
        "solar": {
            "text": "4.8% of total installed capacity (2022 est.)"
        },
        "wind": {
            "text": "10.1% of total installed capacity (2022 est.)"
        },
        "hydroelectricity": {
            "text": "5.8% of total installed capacity (2022 est.)"
        },
        "geothermal": {
            "text": "0.4% of total installed capacity (2022 est.)"
        },
        "biomass and waste": {
            "text": "1.5% of total installed capacity (2022 est.)"
        }
    }
    parsed_data = parse_electricity_sources(electricity_sources_data)
    print(parsed_data)
