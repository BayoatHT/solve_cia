import re
import logging
from typing import Dict, List, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_religions(religion_data: dict, iso3Code: str = None) -> dict:
    """
    Parse religions data from CIA World Factbook format.

    Handles ALL format variations found across 238 countries:
    1. Simple percentages: "Roman Catholic 47%, Muslim 4%, Protestant 2%"
    2. Nested percentages: "Protestant 26.7% (Evangelical 25.5%, other Protestant 1.2%)"
    3. No percentages: "Muslim (official; citizens are 85-90% Sunni)"
    4. With year/estimate: "(2021 est.)" at end
    5. With HTML notes

    Args:
        religion_data: Dictionary with 'text' and optional 'note' keys
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured religions data:
        {
            "religions": [
                {"religion": "Roman Catholic", "percentage": 47.0, "subcategories": None},
                {"religion": "Protestant", "percentage": 26.7, "subcategories": [
                    {"name": "Evangelical", "percentage": 25.5},
                    {"name": "other Protestant", "percentage": 1.2}
                ]}
            ],
            "religions_timestamp": "2021",
            "religions_is_estimate": True,
            "religions_note": ""
        }
    """
    result = {
        "religions": [],
        "religions_timestamp": None,
        "religions_is_estimate": False,
        "religions_note": "",
        "religions_raw": None  # Keep raw text for cases we can't fully parse
    }

    if not religion_data or not isinstance(religion_data, dict):
        return result

    text = religion_data.get('text', '').strip()
    note = religion_data.get('note', '')

    # Clean HTML entities early
    text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    text = re.sub(r'<p>', '', text).replace('</p>', '')

    if not text or text.upper() == 'NA':
        return result

    # Store raw text
    result["religions_raw"] = text

    # Extract year and estimate from end of text
    year_match = re.search(r'\((\d{4})\s*(est\.?)?\)\s*$', text)
    if year_match:
        result["religions_timestamp"] = year_match.group(1)
        result["religions_is_estimate"] = bool(year_match.group(2))
        # Remove year from text for easier parsing
        text = text[:year_match.start()].strip()

    # Clean HTML from note
    if note:
        note = re.sub(r'<[^>]+>', '', note).strip()
        note = re.sub(r'^note:\s*', '', note, flags=re.IGNORECASE)
        result["religions_note"] = note

    # Check if text has percentages
    if '%' not in text:
        # No percentages - store as single descriptive entry
        result["religions"].append({
            "religion": text,
            "percentage": None,
            "subcategories": None,
            "descriptive": True
        })
        return result

    # Parse religions with percentages
    # Strategy: Split by comma, but handle nested parentheses

    def split_religions(text: str) -> List[str]:
        """Split religion text by commas, respecting parentheses and preserving commas in numbers."""
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

    def parse_religion_entry(entry: str) -> Optional[dict]:
        """Parse a single religion entry."""
        entry = entry.strip()
        if not entry:
            return None

        result_entry = {
            "religion": None,
            "percentage": None,
            "subcategories": None
        }

        # Pattern for nested: "Protestant 26.7% (Evangelical 25.5%, other Protestant 1.2%)"
        # Also handles "<1%" (less than) with optional spaces around "<"
        nested_match = re.match(
            r'^([^%]+?)\s*<?\s*([\d.]+)%\s*\(([^)]+)\)\s*$',
            entry
        )

        if nested_match:
            result_entry["religion"] = nested_match.group(1).strip()
            result_entry["percentage"] = float(nested_match.group(2))

            # Parse subcategories
            subcats_text = nested_match.group(3)
            subcats = []
            for subcat in subcats_text.split(','):
                subcat = subcat.strip()
                sub_match = re.match(r'^([^%]+?)\s*<?\s*([\d.]+)%', subcat)
                if sub_match:
                    subcats.append({
                        "name": sub_match.group(1).strip(),
                        "percentage": float(sub_match.group(2))
                    })
                elif subcat:
                    # Subcategory without percentage
                    subcats.append({
                        "name": subcat,
                        "percentage": None
                    })

            if subcats:
                result_entry["subcategories"] = subcats

            return result_entry

        # Pattern for simple: "Roman Catholic 47%" or "Muslim 4%"
        # Also handles "<1%" (less than) with spaces, and trailing comma
        simple_match = re.match(
            r'^([^%]+?)\s*,?\s*<?\s*([\d.]+)%',
            entry
        )

        if simple_match:
            result_entry["religion"] = simple_match.group(1).strip()
            result_entry["percentage"] = float(simple_match.group(2))
            return result_entry

        # Pattern for range: "Muslim (official; citizens are 85-90% Sunni)"
        # Just capture the name without trying to parse range
        if entry and '%' not in entry:
            result_entry["religion"] = entry
            result_entry["descriptive"] = True
            return result_entry

        return None

    # Split and parse each religion
    parts = split_religions(text)

    for part in parts:
        parsed = parse_religion_entry(part)
        if parsed and parsed.get("religion"):
            result["religions"].append(parsed)

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Simple format (USA)
    test1 = {
        "text": "Protestant 46.5%, Roman Catholic 20.8%, Jewish 1.9%, Muslim 0.9%, Buddhist 0.7%, other 1.8%, unaffiliated 22.8% (2014 est.)"
    }
    print("Test 1 - Simple format (USA):")
    result = parse_religions(test1)
    print(f"Found {len(result['religions'])} religions")
    for r in result['religions'][:3]:
        print(f"  {r['religion']}: {r['percentage']}%")
    print()

    # Test Case 2: Nested format (Brazil)
    test2 = {
        "text": "Roman Catholic 52.8%, Protestant 26.7% (Evangelical 25.5%, other Protestant 1.2%), other 3%, none 13.6% (2023 est.)"
    }
    print("Test 2 - Nested format (Brazil):")
    result = parse_religions(test2)
    for r in result['religions']:
        print(f"  {r['religion']}: {r['percentage']}%")
        if r.get('subcategories'):
            for s in r['subcategories']:
                print(f"    -> {s['name']}: {s['percentage']}%")
    print()

    # Test Case 3: No percentages (Saudi Arabia style)
    test3 = {
        "text": "Muslim (official; citizens are 85-90% Sunni and 10-12% Shia)",
        "note": "<strong>note:</strong> large expatriate community of various faiths"
    }
    print("Test 3 - No percentages:")
    result = parse_religions(test3)
    print(f"  Raw: {result['religions_raw'][:50]}...")
    print(f"  Note: {result['religions_note'][:50]}...")
    print()

    # Test Case 4: Empty
    print("Test 4 - Empty:")
    print(parse_religions({}))
