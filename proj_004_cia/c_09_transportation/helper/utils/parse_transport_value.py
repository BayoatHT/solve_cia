"""
Helper function to parse transportation values into structured components.
Extracts numeric value, unit, year, and estimate flag from CIA transportation text.
"""
import re
import logging
from typing import Dict, Any, List, Optional

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_transport_value(text: str) -> Dict[str, Any]:
    """
    Parse transportation value text into structured components.

    Args:
        text: Raw text like "15,873 (2024)" or "41,009 km (2012)"

    Returns:
        Dict with keys:
            - value: float (numeric value with magnitude applied)
            - raw_value: float (original number without magnitude)
            - magnitude: str (billion, million, etc. or None)
            - unit: str (unit of measurement like 'km')
            - year: int (year from parenthesis)
            - is_estimate: bool (whether "est." present)
            - text: str (original cleaned text)

    Examples:
        >>> parse_transport_value("15,873 (2024)")
        {'value': 15873.0, 'unit': None, 'year': 2024, 'is_estimate': False}

        >>> parse_transport_value("41,009 km (2012)")
        {'value': 41009.0, 'unit': 'km', 'year': 2012, 'is_estimate': False}
    """
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

        # Extract year from parenthesis - patterns like (2022 est.) or (2022) or (2022)
        year_match = re.search(r'\((\d{4})(?:\s*est\.?)?\)', clean_text)
        if year_match:
            result['year'] = int(year_match.group(1))

        # Remove the year/estimate portion for further parsing
        text_without_year = re.sub(r'\s*\([^)]*\)\s*', ' ', clean_text).strip()

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

        # Extract numeric value - handle patterns like "15,873" or "41,009.5"
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

            # Clean up unit - just get the first word (km, mt-km, etc.)
            unit_match = re.match(r'^([a-zA-Z\-]+)', unit_text)
            if unit_match:
                result['unit'] = unit_match.group(1)

    except Exception as e:
        logging.error(f"Error parsing transport value '{text}': {e}")

    return result


def parse_pipeline_text(text: str) -> List[Dict[str, Any]]:
    """
    Parse pipeline text with multiple segments.

    Args:
        text: Raw text like "1,984,321 km natural gas, 240,711 km petroleum products (2013)"

    Returns:
        List of dicts with value, unit, type for each pipeline segment

    Example:
        >>> parse_pipeline_text("134 km gas, 27 km refined products (2013)")
        [
            {'value': 134.0, 'unit': 'km', 'type': 'gas'},
            {'value': 27.0, 'unit': 'km', 'type': 'refined products'}
        ]
    """
    pipelines = []

    if not text or not isinstance(text, str):
        return pipelines

    try:
        # Extract year first
        year = None
        year_match = re.search(r'\((\d{4})(?:\s*est\.?)?\)', text)
        if year_match:
            year = int(year_match.group(1))

        # Remove year from text
        text_clean = re.sub(r'\s*\([^)]*\)\s*$', '', text).strip()

        # Split by comma-space followed by a digit (to avoid splitting on commas in numbers)
        # Pattern: ", 240" but not ",321"
        segments = re.split(r',\s+(?=\d)', text_clean)

        for segment in segments:
            segment = segment.strip()
            if not segment:
                continue

            # Pattern: "1,984,321 km natural gas" or "134 km gas"
            match = re.match(r'([\d,]+(?:\.\d+)?)\s+(\w+)\s*(.*)', segment)
            if match:
                value_str = match.group(1).replace(',', '')
                unit = match.group(2) or 'km'
                pipe_type = match.group(3).strip() if match.group(3) else 'unknown'

                pipeline = {
                    'value': float(value_str),
                    'unit': unit,
                    'type': pipe_type
                }
                if year:
                    pipeline['year'] = year

                pipelines.append(pipeline)

    except Exception as e:
        logging.error(f"Error parsing pipeline text '{text}': {e}")

    return pipelines


def parse_subfield_value(data: dict, subfield: str) -> Dict[str, Any]:
    """
    Parse a subfield from transportation data.

    Args:
        data: Dict containing subfields
        subfield: Key to look up

    Returns:
        Parsed value dict
    """
    if not data or subfield not in data:
        return {}

    field_data = data[subfield]

    if isinstance(field_data, dict) and 'text' in field_data:
        return parse_transport_value(field_data['text'])
    elif isinstance(field_data, str):
        return parse_transport_value(field_data)

    return {}


# Example usage and tests
if __name__ == "__main__":
    test_cases = [
        "15,873 (2024)",
        "7,914 (2024)",
        "41,009 km (2012)",
        "293,564.2 km (2014)",
        "889.022 million (2018)",
        "42,985,300,000 mt-km (2018)",
        "3,533 (2023)",
    ]

    print("Testing parse_transport_value:\n")
    for test in test_cases:
        result = parse_transport_value(test)
        print(f"Input: '{test}'")
        print(f"  value: {result['value']}")
        print(f"  unit: {result['unit']}")
        print(f"  year: {result['year']}")
        print()

    print("\nTesting parse_pipeline_text:\n")
    pipeline_tests = [
        "1,984,321 km natural gas, 240,711 km petroleum products (2013)",
        "134 km gas, 27 km refined products (2013)",
        "2,444 km oil (2024)",
    ]

    for test in pipeline_tests:
        result = parse_pipeline_text(test)
        print(f"Input: '{test}'")
        for p in result:
            print(f"  - {p}")
        print()
