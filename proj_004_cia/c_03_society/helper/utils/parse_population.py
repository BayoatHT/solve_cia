import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_population(population_data: dict, iso3Code: str = None) -> dict:
    """
    Parse population data from CIA World Factbook format.

    Handles nested structure:
    {
        "total": {"text": "341,963,408"},
        "male": {"text": "168,598,780"},
        "female": {"text": "173,364,628 (2024 est.)"}
    }

    Args:
        population_data: Dictionary with nested structure
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured population data
    """
    result = {
        "population": {
            "total": None,
            "male": None,
            "female": None,
            "timestamp": None,
            "is_estimate": False
        },
        "population_note": ""
    }

    if not population_data or not isinstance(population_data, dict):
        return result

    # Helper to extract population number and year from text
    def extract_population(text: str) -> tuple:
        if not text or text.upper() == 'NA':
            return None, None, False

        # Pattern: "341,963,408" or "173,364,628 (2024 est.)"
        num_match = re.search(r'([\d,]+)', text)
        year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)

        population = int(num_match.group(1).replace(',', '')) if num_match else None
        year = year_match.group(1) if year_match else None
        is_est = bool(year_match and year_match.group(2)) if year_match else False

        return population, year, is_est

    # Extract total
    if 'total' in population_data:
        total_data = population_data['total']
        text = total_data.get('text', '') if isinstance(total_data, dict) else str(total_data)
        pop, year, is_est = extract_population(text)
        result["population"]["total"] = pop
        if year:
            result["population"]["timestamp"] = year
            result["population"]["is_estimate"] = is_est

    # Extract male
    if 'male' in population_data:
        male_data = population_data['male']
        text = male_data.get('text', '') if isinstance(male_data, dict) else str(male_data)
        pop, year, is_est = extract_population(text)
        result["population"]["male"] = pop
        if year and not result["population"]["timestamp"]:
            result["population"]["timestamp"] = year
            result["population"]["is_estimate"] = is_est

    # Extract female
    if 'female' in population_data:
        female_data = population_data['female']
        text = female_data.get('text', '') if isinstance(female_data, dict) else str(female_data)
        pop, year, is_est = extract_population(text)
        result["population"]["female"] = pop
        if year and not result["population"]["timestamp"]:
            result["population"]["timestamp"] = year
            result["population"]["is_estimate"] = is_est

    # Extract note
    if 'note' in population_data:
        note = population_data['note']
        if isinstance(note, str):
            note = re.sub(r'<[^>]+>', '', note).strip()
            note = re.sub(r'^note\s*\d*:\s*', '', note, flags=re.IGNORECASE)
            result["population_note"] = note

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Full data
    test1 = {
        "total": {"text": "341,963,408"},
        "male": {"text": "168,598,780"},
        "female": {"text": "173,364,628 (2024 est.)"}
    }
    print("Test 1 - Full data:")
    print(parse_population(test1))
    print()

    # Test Case 2: With note
    test2 = {
        "total": {"text": "11,174,024"},
        "male": {"text": "5,844,979"},
        "female": {"text": "5,329,045 (2024 est.)"},
        "note": "<strong>note:</strong> includes refugees"
    }
    print("Test 2 - With note:")
    print(parse_population(test2))
