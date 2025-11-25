import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_infectious_diseases(disease_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parse major infectious diseases from CIA World Factbook format.

    Handles nested structure:
    {
        "degree of risk": {"text": "high (2023)"},
        "food or waterborne diseases": {"text": "bacterial diarrhea, hepatitis A"},
        "vectorborne diseases": {"text": "dengue fever, malaria"},
        ...
    }
    """
    if return_original:
        return disease_data

    result = {
        "infectious_diseases": {
            "degree_of_risk": None,
            "food_or_waterborne": None,
            "vectorborne": None,
            "water_contact": None,
            "respiratory": None,
            "animal_contact": None,
            "timestamp": None
        },
        "infectious_diseases_note": ""
    }

    if not disease_data or not isinstance(disease_data, dict):
        return result

    field_map = {
        'degree of risk': 'degree_of_risk',
        'food or waterborne diseases': 'food_or_waterborne',
        'vectorborne diseases': 'vectorborne',
        'water contact diseases': 'water_contact',
        'respiratory diseases': 'respiratory',
        'animal contact diseases': 'animal_contact'
    }

    for field_name, result_key in field_map.items():
        if field_name in disease_data:
            field_data = disease_data[field_name]
            text = field_data.get('text', '') if isinstance(field_data, dict) else str(field_data)

            if text and text.upper() != 'NA':
                # Extract year from degree of risk
                if field_name == 'degree of risk':
                    year_match = re.search(r'\((\d{4})\)', text)
                    if year_match:
                        result["infectious_diseases"]["timestamp"] = year_match.group(1)
                    # Extract just the risk level
                    risk_match = re.search(r'(high|very high|intermediate|low)', text, re.IGNORECASE)
                    if risk_match:
                        result["infectious_diseases"][result_key] = risk_match.group(1).lower()
                else:
                    result["infectious_diseases"][result_key] = text.strip()

    # Check for note
    if 'note' in disease_data:
        note = disease_data['note']
        if isinstance(note, dict):
            note = note.get('text', '')
        if note:
            note = re.sub(r'<[^>]+>', '', str(note)).strip()
            result["infectious_diseases_note"] = note

    return result


if __name__ == "__main__":
    test1 = {
        "degree of risk": {"text": "high (2023)"},
        "food or waterborne diseases": {"text": "bacterial diarrhea, hepatitis A"},
        "vectorborne diseases": {"text": "dengue fever, malaria"}
    }
    print(parse_infectious_diseases(test1))
