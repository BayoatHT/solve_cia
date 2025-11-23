"""
Parse military personnel data from CIA World Factbook.
"""
import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_military_personnel(military_personnel_data: dict, iso3Code: str = None) -> dict:
    """
    Parses the 'military personnel' data extracting numeric values for each branch.

    Parameters:
        military_personnel_data (dict): Dictionary containing the 'text' field with personnel data.
        iso3Code (str): Country ISO3 code

    Returns:
        dict: Structured dictionary with personnel counts by branch.

    Example:
        Input: "approximately 1.31 million active-duty personnel (446,000 Army; 328,000 Navy...)"
        Output: {
            'personnel_total_value': 1310000,
            'personnel_year': 2024,
            'personnel_branches': [
                {'branch': 'Army', 'value': 446000},
                {'branch': 'Navy', 'value': 328000},
                ...
            ]
        }
    """
    result = {}

    # Extract and clean text
    text = military_personnel_data.get("text", "")
    if not text:
        return result

    try:
        # Store original text
        result['personnel_text'] = clean_text(text)

        # Extract year from text (e.g., "(2024)")
        year_match = re.search(r'\((\d{4})\)', text)
        if year_match:
            result['personnel_year'] = int(year_match.group(1))

        # Magnitude multipliers
        magnitudes = {
            'million': 1_000_000,
            'thousand': 1_000,
        }

        # Extract total personnel - patterns like "1.31 million" or "13,000"
        total_patterns = [
            r'(?:approximately|about|estimated|roughly)?\s*([\d,\.]+)\s*(million|thousand)?\s*(?:active[- ]duty)?\s*personnel',
            r'([\d,\.]+)\s*(million|thousand)?\s*(?:active[- ]duty)?\s*(?:troops|personnel|members)',
        ]

        for pattern in total_patterns:
            total_match = re.search(pattern, text, re.IGNORECASE)
            if total_match:
                value_str = total_match.group(1).replace(',', '')
                value = float(value_str)
                magnitude = total_match.group(2)
                if magnitude:
                    magnitude_lower = magnitude.lower()
                    if magnitude_lower in magnitudes:
                        value *= magnitudes[magnitude_lower]
                result['personnel_total_value'] = int(value)
                break

        # Extract branch breakdowns from parentheses like "(446,000 Army; 328,000 Navy)"
        branches = []
        paren_match = re.search(r'\(([^)]+)\)', text)
        if paren_match:
            paren_text = paren_match.group(1)
            # Split by semicolon and parse each
            parts = re.split(r'[;]', paren_text)
            for part in parts:
                part = part.strip()
                # Pattern: "446,000 Army" or "9,000 Space Force"
                match = re.match(r'([\d,\.]+)\s*(thousand|million)?\s+(.+)', part)
                if match:
                    value_str = match.group(1).replace(',', '')
                    value = float(value_str)
                    magnitude = match.group(2)
                    if magnitude:
                        magnitude_lower = magnitude.lower()
                        if magnitude_lower in magnitudes:
                            value *= magnitudes[magnitude_lower]
                    branch_name = match.group(3).strip()
                    # Clean up branch name
                    branch_name = re.sub(r'\s*\(\d{4}\).*$', '', branch_name).strip()
                    if branch_name and value > 0:
                        branches.append({
                            'branch': branch_name,
                            'value': int(value)
                        })

        if branches:
            result['personnel_branches'] = branches

        # Parse note if present
        if 'note' in military_personnel_data:
            note = military_personnel_data['note']
            if note and isinstance(note, str) and note.strip():
                result['personnel_note'] = clean_text(note)

    except Exception as e:
        logging.error(f"Error parsing military_personnel for {iso3Code}: {e}")

    return result


# Example usage
if __name__ == "__main__":
    military_personnel_data = {
        "text": "approximately 1.31 million active-duty personnel (446,000 Army; 328,000 Navy; 317,000 Air Force; 9,000 Space Force; 167,000 Marine Corps; 40,000 Coast Guard); 330,000 Army National Guard; 105,000 Air National Guard (2024)"
    }
    parsed_data = parse_military_personnel(military_personnel_data)
    print(parsed_data)
