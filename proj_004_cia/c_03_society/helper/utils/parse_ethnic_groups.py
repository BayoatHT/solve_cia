import re
import logging
from typing import Dict, List, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_ethnic_groups(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse ethnic groups data from CIA World Factbook for a given country.

    This parser extracts and structures ethnic group information including:
    - Group names and percentages
    - Subgroups and nested classifications
    - Temporal information (year, estimate status)
    - Descriptive notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured ethnic groups data:
        {
            "ethnic_groups": [{"group": str, "percentage": float, "subgroups": list}],
            "ethnic_groups_timestamp": str,
            "ethnic_groups_is_estimate": bool,
            "ethnic_groups_note": str,
            "ethnic_groups_raw": str
        }

    Examples:
        >>> data = parse_ethnic_groups('USA')
        >>> data['ethnic_groups'][0]
        {'group': 'White', 'percentage': 61.6, 'subgroups': None}

        >>> data = parse_ethnic_groups('CHN')
        >>> data['ethnic_groups'][0]['group']
        'Han Chinese'
    """
    result = {
        "ethnic_groups": [],
        "ethnic_groups_timestamp": None,
        "ethnic_groups_is_estimate": False,
        "ethnic_groups_note": "",
        "ethnic_groups_raw": None
    }

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to People and Society -> Ethnic groups
    society_section = raw_data.get('People and Society', {})
    ethnic_data = society_section.get('Ethnic groups', {})

    if return_original:
        return ethnic_data


    if not ethnic_data or not isinstance(ethnic_data, dict):
        return result

    text = ethnic_data.get('text', '').strip()
    note = ethnic_data.get('note', '')

    # Clean HTML entities early
    text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    text = re.sub(r'<p>', '', text).replace('</p>', '')

    if not text or text.upper() == 'NA':
        return result

    # Store raw text
    result["ethnic_groups_raw"] = text

    # Extract year and estimate from end of text
    year_match = re.search(r'\((\d{4})\s*(est\.?)?\)\s*$', text)
    if year_match:
        result["ethnic_groups_timestamp"] = year_match.group(1)
        result["ethnic_groups_is_estimate"] = bool(year_match.group(2))
        # Remove year from text for easier parsing
        text = text[:year_match.start()].strip()

    # Clean HTML from note
    if note:
        note = re.sub(r'<[^>]+>', '', note).strip()
        note = re.sub(r'^note:\s*', '', note, flags=re.IGNORECASE)
        result["ethnic_groups_note"] = note

    # Check if text has percentages
    if '%' not in text:
        # No percentages - store as single descriptive entry
        result["ethnic_groups"].append({
            "group": text,
            "percentage": None,
            "subgroups": None,
            "descriptive": True
        })
        return result

    # Split by comma, respecting parentheses and preserving commas in numbers
    def split_groups(text: str) -> List[str]:
        parts = []
        current = ""
        paren_depth = 0

        i = 0
        while i < len(text):
            char = text[i]

            if char == '(':
                paren_depth += 1
                current += char
            elif char == ')':
                paren_depth -= 1
                current += char
            elif char == ',' and paren_depth == 0:
                # Check if comma is part of number (e.g., "5,000")
                is_number_comma = False
                if i > 0 and i < len(text) - 1:
                    if text[i-1].isdigit() and text[i+1].isdigit():
                        is_number_comma = True

                if is_number_comma:
                    # Keep the comma as part of the number
                    current += char
                else:
                    # It's a delimiter - split here
                    if current.strip():
                        parts.append(current.strip())
                    current = ""
            else:
                current += char

            i += 1

        if current.strip():
            parts.append(current.strip())

        return parts

    def parse_group_entry(entry: str, return_original: bool = False)-> Optional[dict]:
        if return_original:
            return entry

        entry = entry.strip()
        if not entry:
            return None

        # Handle orphaned percentages like "9.8%" or ", 9.8%" (from bad splits)
        # These should be ignored as they're fragments
        if re.match(r'^,?\s*<?[\d.]+%?\s*$', entry):
            return None

        result_entry = {
            "group": None,
            "percentage": None,
            "subgroups": None
        }

        # Pattern for nested: "ethnic minorities 8.9% (includes Zhang, Hui, Manchu)"
        # Also handles trailing comma and "<1%" with spaces
        nested_match = re.match(
            r'^([^%]+?)\s*,?\s*<?\s*([\d.]+)%\s*\((?:includes?\s*)?([^)]+)\)\s*$',
            entry,
            re.IGNORECASE
        )

        if nested_match:
            result_entry["group"] = nested_match.group(1).strip()
            result_entry["percentage"] = float(nested_match.group(2))
            # Parse subgroups as simple list
            subgroups_text = nested_match.group(3)
            subgroups = [s.strip() for s in re.split(r',\s*(?:and\s+)?', subgroups_text) if s.strip()]
            if subgroups:
                result_entry["subgroups"] = subgroups
            return result_entry

        # Pattern for simple: "White 61.6%" or "Black or African American 12.4%"
        # Also handles "Adamawa, 9.8%" (trailing comma) and "< 1%" (less than with spaces)
        simple_match = re.match(
            r'^([^%]+?)\s*,?\s*<?\s*([\d.]+)%',
            entry
        )

        if simple_match:
            result_entry["group"] = simple_match.group(1).strip()
            result_entry["percentage"] = float(simple_match.group(2))
            return result_entry

        # No percentage - descriptive
        if entry and '%' not in entry:
            result_entry["group"] = entry
            result_entry["descriptive"] = True
            return result_entry

        return None

    # Split and parse each group
    parts = split_groups(text)

    for part in parts:
        parsed = parse_group_entry(part)
        if parsed and parsed.get("group"):
            result["ethnic_groups"].append(parsed)

    return result


if __name__ == "__main__":
    """Test parse_ethnic_groups with real country data."""
    print("="*60)
    print("Testing parse_ethnic_groups across countries")
    print("="*60)

    test_countries = ['USA', 'CHN', 'CMR', 'IND', 'BRA', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_ethnic_groups(iso3)
            groups = result['ethnic_groups']
            print(f"  Found {len(groups)} ethnic group(s)")

            # Show first 3 groups
            for grp in groups[:3]:
                pct = f"{grp['percentage']}%" if grp.get('percentage') else 'N/A'
                subgroups = f" (includes {len(grp.get('subgroups', []))} subgroups)" if grp.get('subgroups') else ""
                print(f"    - {grp['group']}: {pct}{subgroups}")

            if len(groups) > 3:
                print(f"    ... and {len(groups) - 3} more")

            if result.get('ethnic_groups_timestamp'):
                est = " est." if result.get('ethnic_groups_is_estimate') else ""
                print(f"  Timestamp: {result['ethnic_groups_timestamp']}{est}")

            if result.get('ethnic_groups_note'):
                note = result['ethnic_groups_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
