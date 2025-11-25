"""
Helper function to parse energy values into structured components.
Extracts numeric value, unit, year, and estimate flag from CIA energy text.
"""
import re
import logging
from typing import Dict, Any, Optional

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_energy_value(text: str, return_original: bool = False)-> Dict[str, Any]:
    """
    Parse energy value text into structured components.

    Args:
        text: Raw text like "4.941 billion metric tonnes of CO2 (2022 est.)"

    Returns:
        Dict with keys:
            - value: float (numeric value with magnitude applied)
            - raw_value: float (original number without magnitude)
            - magnitude: str (billion, million, trillion, or None)
            - unit: str (unit of measurement)
            - year: int (year from parenthesis)
            - is_estimate: bool (whether "est." present)
            - text: str (original cleaned text)

    Examples:
        >>> parse_energy_value("4.941 billion metric tonnes of CO2 (2022 est.)")
        {
            'value': 4941000000.0,
            'raw_value': 4.941,
            'magnitude': 'billion',
            'unit': 'metric tonnes of CO2',
            'year': 2022,
            'is_estimate': True,
            'text': '4.941 billion metric tonnes of CO2 (2022 est.)'
        }
    """
    if return_original:
        return text

    result = {
        'value': None,
        'raw_value': None,
        'magnitude': None,
        'unit': None,
        'year': None,
        'is_estimate': False,
        'text': None
    }

    if not text or not isinstance(text, str):
        return result

    try:
        # Clean text
        clean_text = text.strip()
        result['text'] = clean_text

        # Check for estimate
        result['is_estimate'] = 'est.' in clean_text.lower() or 'est)' in clean_text.lower()

        # Extract year from parenthesis - patterns like (2022 est.) or (2022)
        year_match = re.search(r'\((\d{4})(?:\s*est\.?)?\)', clean_text)
        if year_match:
            result['year'] = int(year_match.group(1))

        # Remove the year/estimate portion for further parsing
        text_without_year = re.sub(r'\s*\([^)]*\)\s*$', '', clean_text).strip()

        # Magnitude multipliers
        magnitudes = {
            'trillion': 1_000_000_000_000,
            'billion': 1_000_000_000,
            'million': 1_000_000,
            'thousand': 1_000,
        }

        multiplier = 1
        magnitude_found = None
        working_text = text_without_year.lower()

        for mag, mult in magnitudes.items():
            if mag in working_text:
                multiplier = mult
                magnitude_found = mag
                break

        result['magnitude'] = magnitude_found

        # Extract numeric value - handle patterns like "4.941" or "20,879" or "94"
        # First number in the text
        num_match = re.search(r'^[\s]*(-?\d+(?:,\d{3})*(?:\.\d+)?)', text_without_year)
        if num_match:
            raw_value_str = num_match.group(1).replace(',', '')
            raw_value = float(raw_value_str)
            result['raw_value'] = raw_value
            result['value'] = raw_value * multiplier

            # Extract unit - everything after the number and magnitude
            unit_text = text_without_year[num_match.end():].strip()

            # Remove magnitude word from unit
            if magnitude_found:
                unit_text = re.sub(rf'\b{magnitude_found}\b', '', unit_text, flags=re.IGNORECASE).strip()

            # Clean up unit
            unit_text = re.sub(r'^[\s,]+', '', unit_text)  # Remove leading comma/space
            unit_text = re.sub(r'[\s,]+$', '', unit_text)  # Remove trailing comma/space

            if unit_text:
                result['unit'] = unit_text

        # Handle percentage values
        if result['value'] is None:
            pct_match = re.search(r'(\d+(?:\.\d+)?)\s*%', clean_text)
            if pct_match:
                result['raw_value'] = float(pct_match.group(1))
                result['value'] = result['raw_value']
                result['unit'] = '%'

    except Exception as e:
        logging.error(f"Error parsing energy value '{text}': {e}")

    return result


def extract_energy_field(data: dict, field_key: str, output_prefix: str) -> Dict[str, Any]:
    """
    Extract a field from energy data and parse its value.

    Args:
        data: Dict containing field data
        field_key: Key to look up in data
        output_prefix: Prefix for output keys

    Returns:
        Dict with parsed components using output_prefix
    """
    result = {}

    if not data or not isinstance(data, dict):
        return result

    if field_key not in data:
        return result

    field_data = data[field_key]
    if isinstance(field_data, dict) and 'text' in field_data:
        text = field_data['text']
        if text and isinstance(text, str):
            parsed = parse_energy_value(text)

            if parsed['value'] is not None:
                result[f'{output_prefix}_value'] = parsed['value']
            if parsed['raw_value'] is not None:
                result[f'{output_prefix}_raw'] = parsed['raw_value']
            if parsed['magnitude']:
                result[f'{output_prefix}_magnitude'] = parsed['magnitude']
            if parsed['unit']:
                result[f'{output_prefix}_unit'] = parsed['unit']
            if parsed['year']:
                result[f'{output_prefix}_year'] = parsed['year']
            if parsed['is_estimate']:
                result[f'{output_prefix}_is_estimate'] = parsed['is_estimate']
            if parsed['text']:
                result[f'{output_prefix}_text'] = parsed['text']

    return result


# Example usage and tests
if __name__ == "__main__":
    test_cases = [
        "4.941 billion metric tonnes of CO2 (2022 est.)",
        "548.849 million metric tons (2022 est.)",
        "4.128 trillion kWh (2022 est.)",
        "284.575 million Btu/person (2022 est.)",
        "20.879 million bbl/day (2023 est.)",
        "94 (2023)",
        "100% (2022 est.)",
        "18.5% (2023 est.)",
        "96.95GW (2023 est.)",
    ]

    print("Testing parse_energy_value:\n")
    for test in test_cases:
        result = parse_energy_value(test)
        print(f"Input: '{test}'")
        print(f"  value: {result['value']}")
        print(f"  raw_value: {result['raw_value']}")
        print(f"  magnitude: {result['magnitude']}")
        print(f"  unit: {result['unit']}")
        print(f"  year: {result['year']}")
        print(f"  is_estimate: {result['is_estimate']}")
        print()
