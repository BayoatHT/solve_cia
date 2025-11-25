import re
import logging
from typing import Dict, List, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_languages(languages_data: dict, iso3Code: str = None) -> dict:
    """
    Parse languages data from CIA World Factbook format.

    Handles ALL format variations:
    1. Direct 'text' key: {"text": "English 78.2%, Spanish 13.4%"}
    2. Nested 'Languages' key: {"Languages": {"text": "..."}}
    3. With percentages: "Hindi 43.6%, Bengali 8%"
    4. With (official) marker: "French (official) 100%"
    5. With dialects: "declining regional dialects (Provencal, Breton...)"
    6. Major language samples
    7. HTML notes

    Args:
        languages_data: Dictionary with 'text' or 'Languages' key
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured languages data
    """
    result = {
        "languages": [],
        "languages_timestamp": None,
        "languages_is_estimate": False,
        "languages_note": "",
        "languages_raw": None,
        "major_language_samples": []
    }

    if not languages_data or not isinstance(languages_data, dict):
        return result

    # Handle different structures
    # Structure 1: Direct text key
    # Structure 2: Nested Languages key
    if 'Languages' in languages_data:
        lang_obj = languages_data['Languages']
        text = lang_obj.get('text', '') if isinstance(lang_obj, dict) else ''
    elif 'text' in languages_data:
        text = languages_data.get('text', '')
    else:
        return result

    text = text.strip()

    # Clean HTML entities early
    text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')

    # Handle note (can be at top level or nested)
    note = languages_data.get('note', '')
    if note:
        note = re.sub(r'<[^>]+>', '', note).strip()
        note = re.sub(r'^note\s*\d*:\s*', '', note, flags=re.IGNORECASE)
        result["languages_note"] = note

    # Handle major language samples
    if 'major-language sample(s)' in languages_data:
        sample_data = languages_data['major-language sample(s)']
        sample_text = sample_data.get('text', '') if isinstance(sample_data, dict) else ''
        if sample_text:
            # Clean HTML and extract language samples
            sample_text = re.sub(r'<br\s*/?>', '\n', sample_text)
            sample_text = re.sub(r'<[^>]+>', '', sample_text).strip()
            # Split by double newline to get separate language samples
            samples = [s.strip() for s in sample_text.split('\n\n') if s.strip()]
            for sample in samples:
                # Try to extract language name from parentheses
                lang_match = re.search(r'\(([^)]+)\)\s*$', sample)
                if lang_match:
                    result["major_language_samples"].append({
                        "language": lang_match.group(1),
                        "sample": sample[:sample.rfind('(')].strip()
                    })
                elif sample:
                    result["major_language_samples"].append({
                        "language": None,
                        "sample": sample
                    })

    if not text or text.upper() == 'NA':
        return result

    # Store raw text
    result["languages_raw"] = text

    # Extract year and estimate from end
    year_match = re.search(r'\((\d{4})\s*(est\.?)?\)\s*$', text)
    if year_match:
        result["languages_timestamp"] = year_match.group(1)
        result["languages_is_estimate"] = bool(year_match.group(2))
        text = text[:year_match.start()].strip()

    # Check if text has percentages
    if '%' not in text:
        # No percentages - store as descriptive
        result["languages"].append({
            "language": text,
            "percentage": None,
            "is_official": False,
            "dialects": None,
            "descriptive": True
        })
        return result

    # Split by comma/semicolon, respecting parentheses and number patterns
    def split_languages(text: str) -> List[str]:
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
            elif (char == ',' or char == ';') and paren_depth == 0:
                # Check if this comma is part of a number (e.g., "5,000")
                # Look behind and ahead for digits
                is_number_comma = False
                if i > 0 and i < len(text) - 1:
                    prev_char = text[i-1]
                    next_char = text[i+1]
                    if prev_char.isdigit() and next_char.isdigit():
                        is_number_comma = True

                if is_number_comma:
                    # Keep the comma as part of current segment
                    current += char
                else:
                    # It's a delimiter
                    if current.strip():
                        parts.append(current.strip())
                    current = ""
            else:
                current += char

            i += 1

        if current.strip():
            parts.append(current.strip())

        return parts

    def parse_language_entry(entry: str) -> Optional[dict]:
        entry = entry.strip()
        if not entry:
            return None

        result_entry = {
            "language": None,
            "percentage": None,
            "is_official": False,
            "dialects": None
        }

        # Check for (official) marker
        is_official = '(official)' in entry.lower() or 'official' in entry.lower()
        result_entry["is_official"] = is_official

        # Pattern: "French (official) 100%" or "Hindi 43.6%"
        # Handle complex patterns like "declining regional dialects (Provencal, Breton)"

        # Try pattern with percentage
        pct_match = re.search(r'([\d.]+)%', entry)
        if pct_match:
            result_entry["percentage"] = float(pct_match.group(1))
            # Extract language name (everything before the percentage, cleaned up)
            name_part = entry[:pct_match.start()].strip()
            # Remove (official) and trailing noise
            name_part = re.sub(r'\s*\(official\)\s*', ' ', name_part, flags=re.IGNORECASE).strip()
            name_part = re.sub(r'\s*only\s*$', '', name_part, flags=re.IGNORECASE).strip()
            result_entry["language"] = name_part
            return result_entry

        # Check for speaker count pattern (e.g., "<5,000 speakers" or "5,000 speakers")
        # This should be treated as descriptive info, not split
        speakers_match = re.search(r'(<?\d[\d,]*)\s+(speakers|native speakers)', entry, re.IGNORECASE)
        if speakers_match:
            # Extract language name (everything before the speaker count)
            name_part = entry[:speakers_match.start()].strip()
            # Clean up trailing punctuation and official markers
            name_part = re.sub(r'\s*\(official[^)]*\)\s*$', '', name_part, flags=re.IGNORECASE).strip()
            result_entry["language"] = name_part if name_part else entry
            result_entry["descriptive"] = True
            return result_entry

        # No percentage - check for dialects pattern
        dialect_match = re.match(
            r'^([^(]+)\s*\(([^)]+)\)\s*$',
            entry
        )
        if dialect_match:
            result_entry["language"] = dialect_match.group(1).strip()
            paren_content = dialect_match.group(2).strip().lower()
            # Check if parentheses content is just "official" marker
            if paren_content == 'official' or 'official' in paren_content and len(paren_content) < 30:
                # It's an official marker, not dialects
                result_entry["is_official"] = True
                result_entry["descriptive"] = True
            else:
                # Actual dialects
                dialects = [d.strip() for d in dialect_match.group(2).split(',') if d.strip()]
                result_entry["dialects"] = dialects
                result_entry["descriptive"] = True
            return result_entry

        # Simple language name without percentage
        if entry and '%' not in entry:
            # Clean up official markers
            clean_entry = re.sub(r'\s*\(official\)\s*', '', entry, flags=re.IGNORECASE).strip()
            result_entry["language"] = clean_entry
            result_entry["descriptive"] = True
            return result_entry

        return None

    # Split and parse
    parts = split_languages(text)

    for part in parts:
        parsed = parse_language_entry(part)
        if parsed and parsed.get("language"):
            result["languages"].append(parsed)

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: USA format (direct text)
    test1 = {
        "text": "English only 78.2%, Spanish 13.4%, Chinese 1.1%, other 7.3% (2017 est.)",
        "note": "<strong>note:</strong> data represent language spoken at home"
    }
    print("Test 1 - USA format:")
    result = parse_languages(test1)
    print(f"Found {len(result['languages'])} languages")
    for l in result['languages'][:3]:
        print(f"  {l['language']}: {l['percentage']}%")
    print(f"Note: {result['languages_note'][:40]}...")
    print()

    # Test Case 2: France format (nested with dialects)
    test2 = {
        "Languages": {
            "text": "French (official) 100%, declining regional dialects (Provencal, Breton, Alsatian)"
        },
        "major-language sample(s)": {
            "text": "<br>The World Factbook (French)<br><br>English translation"
        }
    }
    print("Test 2 - France format (nested):")
    result = parse_languages(test2)
    for l in result['languages']:
        print(f"  {l['language']}: {l['percentage']}%, official={l['is_official']}")
        if l.get('dialects'):
            print(f"    Dialects: {l['dialects'][:3]}")
    print()

    # Test Case 3: India format (many languages)
    test3 = {
        "Languages": {
            "text": "Hindi 43.6%, Bengali 8%, Marathi 6.9%, Telugu 6.7% (2011 est.)"
        }
    }
    print("Test 3 - India format:")
    result = parse_languages(test3)
    print(f"Found {len(result['languages'])} languages, timestamp={result['languages_timestamp']}")
    print()

    # Test Case 4: Empty
    print("Test 4 - Empty:")
    print(parse_languages({}))
