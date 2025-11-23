import re
import logging
from typing import Dict, List, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_ethnic_groups(ethnic_data: dict, iso3Code: str = None) -> dict:
    """
    Parse ethnic groups data from CIA World Factbook format.

    Handles ALL format variations found across countries:
    1. Simple percentages: "White 61.6%, Black 12.4%, Asian 6%"
    2. Nested groups: "Han Chinese 91.1%, minorities 8.9% (includes Zhang, Hui...)"
    3. No percentages: "Celtic and Latin with Teutonic, Slavic..."
    4. With year/estimate: "(2020 est.)" at end
    5. With HTML notes

    Args:
        ethnic_data: Dictionary with 'text' and optional 'note' keys
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured ethnic groups data:
        {
            "ethnic_groups": [
                {"group": "White", "percentage": 61.6, "subgroups": None},
                {"group": "ethnic minorities", "percentage": 8.9, "subgroups": ["Zhang", "Hui"]}
            ],
            "ethnic_groups_timestamp": "2020",
            "ethnic_groups_is_estimate": True,
            "ethnic_groups_note": ""
        }
    """
    result = {
        "ethnic_groups": [],
        "ethnic_groups_timestamp": None,
        "ethnic_groups_is_estimate": False,
        "ethnic_groups_note": "",
        "ethnic_groups_raw": None
    }

    if not ethnic_data or not isinstance(ethnic_data, dict):
        return result

    text = ethnic_data.get('text', '').strip()
    note = ethnic_data.get('note', '')

    if not text or text.upper() == 'NA':
        return result

    # Store raw text
    result["ethnic_groups_raw"] = text

    # Extract year and estimate from end of text
    year_match = re.search(r'\((\d{4})\s*(est\.?)?\)\s*$', text)
    if year_match:
        result["ethnic_groups_timestamp"] = year_match.group(1)
        result["ethnic_groups_is_estimate"] = bool(year_match.group(2))
        text = text[:year_match.start()].strip()

    # Clean HTML from note
    if note:
        note = re.sub(r'<[^>]+>', '', note).strip()
        note = re.sub(r'^note:\s*', '', note, flags=re.IGNORECASE)
        result["ethnic_groups_note"] = note

    # Check if text has percentages
    if '%' not in text:
        # No percentages - store as descriptive
        result["ethnic_groups"].append({
            "group": text,
            "percentage": None,
            "subgroups": None,
            "descriptive": True
        })
        return result

    # Split by comma, respecting parentheses
    def split_groups(text: str) -> List[str]:
        parts = []
        current = ""
        paren_depth = 0

        for char in text:
            if char == '(':
                paren_depth += 1
                current += char
            elif char == ')':
                paren_depth -= 1
                current += char
            elif char == ',' and paren_depth == 0:
                if current.strip():
                    parts.append(current.strip())
                current = ""
            else:
                current += char

        if current.strip():
            parts.append(current.strip())

        return parts

    def parse_group_entry(entry: str) -> Optional[dict]:
        entry = entry.strip()
        if not entry:
            return None

        result_entry = {
            "group": None,
            "percentage": None,
            "subgroups": None
        }

        # Pattern for nested: "ethnic minorities 8.9% (includes Zhang, Hui, Manchu)"
        nested_match = re.match(
            r'^([^%]+?)\s*([\d.]+)%\s*\((?:includes?\s*)?([^)]+)\)\s*$',
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
        simple_match = re.match(
            r'^([^%]+?)\s*([\d.]+)%',
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


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: USA format
    test1 = {
        "text": "White 61.6%, Black or African American 12.4%, Asian 6%, other 8.4%, two or more races 10.2% (2020 est.)",
        "note": "<strong>note:</strong> Hispanic not included separately"
    }
    print("Test 1 - USA format:")
    result = parse_ethnic_groups(test1)
    print(f"Found {len(result['ethnic_groups'])} groups")
    for g in result['ethnic_groups'][:3]:
        print(f"  {g['group']}: {g['percentage']}%")
    print()

    # Test Case 2: China format (nested)
    test2 = {
        "text": "Han Chinese 91.1%, ethnic minorities 8.9% (includes Zhang, Hui, Manchu, Uighur) (2021 est.)"
    }
    print("Test 2 - China format (nested):")
    result = parse_ethnic_groups(test2)
    for g in result['ethnic_groups']:
        print(f"  {g['group']}: {g['percentage']}%")
        if g.get('subgroups'):
            print(f"    Subgroups: {g['subgroups'][:4]}...")
    print()

    # Test Case 3: France (no percentages)
    test3 = {
        "text": "Celtic and Latin with Teutonic, Slavic, North African minorities"
    }
    print("Test 3 - France (no percentages):")
    result = parse_ethnic_groups(test3)
    print(f"  Descriptive: {result['ethnic_groups'][0]['group'][:50]}...")
    print()

    # Test Case 4: Empty
    print("Test 4 - Empty:")
    print(parse_ethnic_groups({}))
