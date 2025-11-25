import re
import logging
from typing import Dict, List, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_languages(iso3Code: str) -> dict:
    """
    Parse languages data from CIA World Factbook for a given country.

    This parser extracts and structures language information including:
    - Language names and percentages
    - Official language markers
    - Regional dialects
    - Speaker counts
    - Major language samples
    - Temporal information (year, estimate status)

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'FRA', 'WLD')

    Returns:
        Dictionary with structured languages data:
        {
            "languages": [{"language": str, "percentage": float, "is_official": bool, ...}],
            "languages_timestamp": str,
            "languages_is_estimate": bool,
            "languages_note": str,
            "languages_raw": str,
            "major_language_samples": [{"language": str, "sample": str}]
        }

    Examples:
        >>> data = parse_languages('USA')
        >>> data['languages'][0]
        {'language': 'English', 'percentage': 78.2, 'is_official': False}

        >>> data = parse_languages('FRA')
        >>> data['languages'][0]['is_official']
        True
    """
    result = {
        "languages": [],
        "languages_timestamp": None,
        "languages_is_estimate": False,
        "languages_note": "",
        "languages_raw": None,
        "major_language_samples": []
    }

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to People and Society -> Languages
    society_section = raw_data.get('People and Society', {})
    languages_data = society_section.get('Languages', {})

    if not languages_data or not isinstance(languages_data, dict):
        return result

    # Handle nested structure: Languages -> Languages -> text vs Languages -> text
    if 'Languages' in languages_data and isinstance(languages_data['Languages'], dict):
        lang_content = languages_data['Languages']
    else:
        lang_content = languages_data

    # Extract text field
    text = lang_content.get('text', '').strip()

    # Clean HTML entities early and remove HTML tags
    text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    text = text.replace('<p>', '').replace('</p>', '').replace('<strong>', '').replace('</strong>', '')

    # Handle note (can be in parent languages_data or lang_content)
    note = languages_data.get('note', '') or lang_content.get('note', '')
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

        # Check for speaker count pattern
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
        dialect_match = re.match(r'^([^(]+)\s*\(([^)]+)\)\s*$', entry)
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


if __name__ == "__main__":
    """Test parse_languages with real country data."""
    print("="*60)
    print("Testing parse_languages across countries")
    print("="*60)

    test_countries = ['USA', 'FRA', 'IND', 'CHN', 'ESP', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_languages(iso3)
            langs = result['languages']
            print(f"  Found {len(langs)} language(s)")

            # Show first 3 languages
            for lang in langs[:3]:
                pct = f"{lang['percentage']}%" if lang.get('percentage') else 'N/A'
                official = " (official)" if lang.get('is_official') else ""
                print(f"    - {lang['language']}: {pct}{official}")

            if len(langs) > 3:
                print(f"    ... and {len(langs) - 3} more")

            if result.get('languages_timestamp'):
                est = " est." if result.get('languages_is_estimate') else ""
                print(f"  Timestamp: {result['languages_timestamp']}{est}")

            if result.get('languages_note'):
                note = result['languages_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
