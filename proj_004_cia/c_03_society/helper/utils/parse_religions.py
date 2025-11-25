import re
import logging
from typing import Dict, List, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_religions(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse religions data from CIA World Factbook for a given country.

    This parser extracts and structures religion information including:
    - Religion names and percentages
    - Subcategories and nested classifications
    - Temporal information (year, estimate status)
    - Descriptive notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'BRA', 'WLD')

    Returns:
        Dictionary with structured religions data:
        {
            "religions": [{"religion": str, "percentage": float, "subcategories": list}],
            "religions_timestamp": str,
            "religions_is_estimate": bool,
            "religions_note": str,
            "religions_raw": str
        }

    Examples:
        >>> data = parse_religions('USA')
        >>> data['religions'][0]
        {'religion': 'Protestant', 'percentage': 46.5, 'subcategories': None}

        >>> data = parse_religions('BRA')
        >>> len(data['religions'][1].get('subcategories', []))
        2
    """
    result = {
        "religions": [],
        "religions_timestamp": None,
        "religions_is_estimate": False,
        "religions_note": "",
        "religions_raw": None  # Keep raw text for cases we can't fully parse
    }

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to People and Society -> Religions
    society_section = raw_data.get('People and Society', {})
    religion_data = society_section.get('Religions', {})

    if return_original:
        return religion_data


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

    def parse_religion_entry(entry: str, return_original: bool = False)-> Optional[dict]:
        """Parse a single religion entry."""
        if return_original:
            return entry

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


if __name__ == "__main__":
    """Test parse_religions with real country data."""
    print("="*60)
    print("Testing parse_religions across countries")
    print("="*60)

    test_countries = ['USA', 'BRA', 'CHN', 'LBY', 'SAU', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_religions(iso3)
            religions = result['religions']
            print(f"  Found {len(religions)} religion(s)")

            # Show first 3 religions
            for rel in religions[:3]:
                pct = f"{rel['percentage']}%" if rel.get('percentage') else 'N/A'
                subcats = f" (includes {len(rel.get('subcategories', []))} subcategories)" if rel.get('subcategories') else ""
                print(f"    - {rel['religion']}: {pct}{subcats}")

            if len(religions) > 3:
                print(f"    ... and {len(religions) - 3} more")

            if result.get('religions_timestamp'):
                est = " est." if result.get('religions_is_estimate') else ""
                print(f"  Timestamp: {result['religions_timestamp']}{est}")

            if result.get('religions_note'):
                note = result['religions_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
