import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_urbanization(urban_data: dict, iso3Code: str = None) -> dict:
    """Parse urbanization data from Environment section."""
    result = {
        "env_urbanization": {
            "urban_population_percent": None,
            "urban_population_year": None,
            "rate_of_urbanization": None,
            "rate_period": None,
            "is_estimate": False
        },
        "env_urbanization_note": ""
    }

    if not urban_data or not isinstance(urban_data, dict):
        return result

    # Parse urban population
    pop_data = urban_data.get('urban population', {})
    if pop_data and isinstance(pop_data, dict):
        text = pop_data.get('text', '')
        if text and text.upper() != 'NA':
            pct_match = re.search(r'([\d.]+)%', text)
            if pct_match:
                result['env_urbanization']['urban_population_percent'] = float(pct_match.group(1))
            year_match = re.search(r'\((\d{4})\)', text)
            if year_match:
                result['env_urbanization']['urban_population_year'] = year_match.group(1)

    # Parse rate of urbanization
    rate_data = urban_data.get('rate of urbanization', {})
    if rate_data and isinstance(rate_data, dict):
        text = rate_data.get('text', '')
        if text and text.upper() != 'NA':
            rate_match = re.search(r'(-?[\d.]+)%', text)
            if rate_match:
                result['env_urbanization']['rate_of_urbanization'] = float(rate_match.group(1))
            period_match = re.search(r'\((\d{4}-\d{2,4})\s*(est\.?)?\)', text)
            if period_match:
                result['env_urbanization']['rate_period'] = period_match.group(1)
                result['env_urbanization']['is_estimate'] = 'est' in text.lower()

    note = urban_data.get('note', '')
    if note:
        result['env_urbanization_note'] = clean_text(note) if isinstance(note, str) else clean_text(note.get('text', ''))

    return result


if __name__ == "__main__":
    test_data = {
        "urban population": {"text": "83.3% of total population (2023)"},
        "rate of urbanization": {"text": "0.96% annual rate of change (2020-25 est.)"}
    }
    print(parse_urbanization(test_data))
