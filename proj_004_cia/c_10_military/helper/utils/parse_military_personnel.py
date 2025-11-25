"""
Parse military personnel data from CIA World Factbook.
"""
import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_military_personnel(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse military personnel data from CIA Military and Security section.

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN')

    Returns:
        dict: Structured dictionary with personnel counts by branch.

    Example:
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

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    military_section = raw_data.get('Military and Security', {})
    military_personnel_data = military_section.get('Military and security service personnel strengths', {})

    if return_original:
        return military_personnel_data


    if not military_personnel_data or not isinstance(military_personnel_data, dict):
        return result

    try:
        # Extract and clean text
        text = military_personnel_data.get("text", "")
        if not text:
            return result

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
        logger.error(f"Error parsing military_personnel for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Testing parse_military_personnel")
    print("=" * 60)
    for iso3 in ['USA', 'CHN', 'RUS', 'IND', 'FRA', 'GBR']:
        print(f"\n{iso3}:")
        try:
            result = parse_military_personnel(iso3)
            if result.get('personnel_total_value'):
                total = result['personnel_total_value']
                year = result.get('personnel_year', '')
                print(f"  Total: {total:,} ({year})")
                if result.get('personnel_branches'):
                    for b in result['personnel_branches'][:3]:
                        print(f"    {b['branch']}: {b['value']:,}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "=" * 60)
    print("✓ Tests complete")
