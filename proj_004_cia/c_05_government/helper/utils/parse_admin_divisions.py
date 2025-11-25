import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._save_test_data_as_text import save_test_data_as_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def clean_text(text: str, preserve_special_chars: bool = False) -> str:
    """Enhanced text cleaning for administrative divisions"""
    if not text:
        return ""

    # Handle HTML entities first
    html_entities = {
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&apos;': "'",
        '&eacute;': 'é',
        '&uacute;': 'ú'
    }

    for entity, replacement in html_entities.items():
        text = text.replace(entity, replacement)

    if not preserve_special_chars:
        # Remove HTML tags but preserve content
        text = re.sub(r'<[^>]+>', '', text)

    # Normalize whitespace
    text = ' '.join(text.split())
    return text.strip()


def extract_division_count(text: str) -> Optional[int]:
    """Extract the count of administrative divisions from text"""
    # Handle complex patterns like "50 states and 1 district", "81 provinces", etc.

    # First try to match the main pattern at the beginning
    main_pattern = r'^(\d+)\s+(?:states?|provinces?|regions?|departments?|counties?|districts?|territories?|governorates?|municipalities?|cantons?|parishes?|oblasts?|divisions?|voivodships?|autonomous|prefectures?|boroughs?|councils?)'

    match = re.search(main_pattern, text, re.IGNORECASE)
    if match:
        return int(match.group(1))

    # Try to extract from "X and Y" patterns
    and_pattern = r'^(\d+)\s+\w+\s+and\s+(\d+)\s+\w+'
    match = re.search(and_pattern, text, re.IGNORECASE)
    if match:
        return int(match.group(1)) + int(match.group(2))

    # Handle special cases like "none" or complex descriptions
    if text.lower().startswith('none'):
        return 0

    return None


def extract_divisions_from_text(text: str, iso3Code: str = None) -> List[str]:
    """
    Extract clean division names from administrative division text

    Args:
        text: Raw text containing administrative divisions
        iso3Code: Country code for special case handling

    Returns:
        List of clean division names only
    """
    if not text:
        return []

    # Clean HTML tags first
    text = re.sub(r'</?(?:p|strong|em)[^>]*>', '', text)
    text = clean_text(text, preserve_special_chars=True)

    # Handle special cases where divisions aren't listed
    if any(phrase in text.lower() for phrase in [
        'none (territory', 'none (overseas', 'none (part of',
        'none (commonwealth', 'none (administered', 'none (special'
    ]):
        return []

    # Handle complex "none" cases that do have divisions listed
    if text.lower().startswith('none ') and ' but there are ' in text.lower():
        # Extract from the "but there are" part
        but_match = re.search(
            r'but there are[^;]*;\s*(.+)', text, re.IGNORECASE)
        if but_match:
            text = but_match.group(1)

    # Split metadata from actual divisions using semicolon
    # Pattern: "X administrative_units (details); Division1, Division2, ..."
    if ';' in text:
        semicolon_index = text.find(';')
        metadata_part = text[:semicolon_index].strip()
        divisions_part = text[semicolon_index + 1:].strip()

        # Check if the first part is metadata (contains count + administrative unit type)
        metadata_patterns = [
            r'^\d+\s+(?:administrative\s+)?(?:states?|provinces?|regions?|departments?|counties?|districts?|territories?|governorates?|municipalities?|cantons?|parishes?|oblasts?|divisions?|voivodships?|autonomous|prefectures?|boroughs?|councils?|communes?|emirates?|atolls?|islands?)',
            r'^none\s*\([^)]*\)',
            r'^\d+\s+[^,;]+\s+(?:and|,)\s+\d+\s+[^;]*'
        ]

        is_metadata = any(re.search(pattern, metadata_part, re.IGNORECASE)
                          for pattern in metadata_patterns)

        if is_metadata and divisions_part:
            # Use the divisions part
            text = divisions_part

    # Remove remaining descriptive text patterns
    # Remove "note" clauses that aren't division names
    text = re.sub(
        r';\s*note\s*[-:]?[^;,]*(?:implementation|US Board|Geographic Names)[^;,]*', '', text, flags=re.IGNORECASE)
    text = re.sub(
        r'note\s*[-:]?[^;,]*(?:administrative|divisions|defined)[^;,]*;\s*', '', text, flags=re.IGNORECASE)

    # Remove introductory explanatory text
    text = re.sub(r'^[^;,]*\([^)]*administrative[^)]*\);\s*',
                  '', text, flags=re.IGNORECASE)
    text = re.sub(
        r'^there are no first-order[^;]*;\s*', '', text, flags=re.IGNORECASE)

    # Determine best delimiter
    delimiter = ','
    # Use semicolon if it appears to separate actual divisions (not just metadata)
    if ';' in text:
        # Count meaningful semicolons (not in parentheses)
        semicolons_outside_parens = len(re.findall(r';(?![^()]*\))', text))
        commas_outside_parens = len(re.findall(r',(?![^()]*\))', text))

        if semicolons_outside_parens > 0 and semicolons_outside_parens >= commas_outside_parens / 3:
            delimiter = ';'

    # Split by delimiter
    divisions = [item.strip() for item in text.split(delimiter)]

    # Clean each division
    cleaned_divisions = []
    for division in divisions:
        if not division:
            continue

        # Skip clearly non-division text
        skip_patterns = [
            r'^note\s*[-:]?',
            r'^there are no',
            r'^administrative divisions',
            r'^the \d+ statistical',
            r'as defined by',
            r'but there are',
            r'at the second order',
            r'includes? main island',
            r'following the',
            r'see separate entries'
        ]

        if any(re.search(pattern, division, re.IGNORECASE) for pattern in skip_patterns):
            continue

        # Remove leading numbers, bullets, and excess whitespace
        division = re.sub(r'^\d+\.\s*', '', division)
        division = re.sub(r'^[•\-*]\s*', '', division)
        division = division.strip()

        # Skip very short entries or meaningless connectors
        if (len(division) <= 2 or
            division.lower() in ['and', 'or', 'note', 'see', 'also', 'with', 'the'] or
                re.match(r'^[^\w]*$', division)):  # Only punctuation/symbols
            continue

        # Handle special formatting like "includes main island of Taiwan plus..."
        if 'includes main island' in division.lower():
            continue

        cleaned_divisions.append(division)

    return cleaned_divisions


def parse_html_categorized_divisions(text: str, return_original: bool = False)-> Dict[str, Any]:
    """Parse HTML-formatted categorized administrative divisions"""
    if return_original:
        return text

    categories = {}

    # Remove outer <p> tags first
    text = re.sub(r'^<p>|</p>$', '', text)

    # Split by paragraph or line breaks to handle different HTML structures
    sections = re.split(r'</?p[^>]*>|\n\n|<br\s*/?>(?:<br\s*/?>)?', text)
    sections = [s.strip() for s in sections if s.strip()]

    for section in sections:
        # Look for category headers like "<strong>provinces:</strong>" or "**provinces:**"
        category_patterns = [
            r'<strong>([^:]+):</strong>\s*(.+)',
            r'\*\*([^:]+):\*\*\s*(.+)',
            r'<em>([^:]+):</em>\s*(.+)'
        ]

        for pattern in category_patterns:
            category_match = re.search(
                pattern, section, re.IGNORECASE | re.DOTALL)
            if category_match:
                category_name = clean_text(category_match.group(1))
                category_content = clean_text(category_match.group(2))

                # Parse the list of divisions
                divisions = extract_divisions_from_text(category_content)

                if divisions:
                    categories[category_name] = {
                        "count": len(divisions),
                        "divisions": divisions
                    }
                break

    return categories


def extract_territorial_info(text: str) -> Dict[str, Any]:
    """Extract territorial and administrative information"""
    info = {
        "is_territory": False,
        "parent_country": None,
        "territorial_status": None,
        "special_notes": []
    }

    # Territory patterns
    territory_patterns = [
        r'territory of the (\w+)',
        r'part of the Kingdom of the (\w+)',
        r'overseas territory of the (\w+)',
        r'commonwealth in political union with the (\w+)',
        r'administered by the (\w+)',
        r'special administrative region of[^(]*\(([^)]+)\)'
    ]

    text_lower = text.lower()

    for pattern in territory_patterns:
        match = re.search(pattern, text_lower)
        if match:
            info["is_territory"] = True
            info["parent_country"] = match.group(1).upper()
            break

    # Extract territorial status
    if 'territory of' in text_lower:
        info["territorial_status"] = "territory"
    elif 'overseas' in text_lower:
        info["territorial_status"] = "overseas_territory"
    elif 'commonwealth' in text_lower:
        info["territorial_status"] = "commonwealth"
    elif 'autonomous' in text_lower:
        info["territorial_status"] = "autonomous_region"
    elif 'special administrative region' in text_lower:
        info["territorial_status"] = "special_administrative_region"

    return info


def parse_special_cases(text: str, iso3Code: str, return_original: bool = False)-> Dict[str, Any]:
    """Handle special cases for specific countries"""
    if return_original:
        return text


    # Special handling for territories with "none" but actual divisions
    none_with_divisions_codes = ['ASM', 'MNP', 'PRI', 'VIR']
    if iso3Code in none_with_divisions_codes:
        if 'but there are' in text.lower():
            divisions = extract_divisions_from_text(text, iso3Code)
            territorial_info = extract_territorial_info(text)
            return {
                "type": "territory_with_divisions",
                "territorial_info": territorial_info,
                "divisions": divisions,
                "division_count": len(divisions),
                "unit_type": "second_order_divisions",
                "explanation": "No first-order divisions, but has second-order administrative units"
            }

    # Handle pure "none" cases
    pure_none_codes = ['CCK', 'GUM', 'CXR', 'NFK', 'COK',
                       'VAT', 'TKL', 'PCN', 'GIB', 'AIA', 'TCA', 'VGB']
    if iso3Code in pure_none_codes or text.lower().strip() == 'none':
        territorial_info = extract_territorial_info(text)
        return {
            "type": "no_divisions",
            "territorial_info": territorial_info,
            "explanation": "No administrative divisions"
        }

    # Handle complex territorial descriptions (like Western Sahara)
    if iso3Code == 'ESH':  # Western Sahara
        return {
            "type": "disputed_territory",
            "status": "contested_sovereignty",
            "description": clean_text(text),
            "administered_by": "Morocco (de facto)",
            "claimed_by": "Sahrawi Arab Democratic Republic"
        }

    # Handle Falkland Islands
    if iso3Code == 'FLK':
        return {
            "type": "disputed_territory",
            "administered_by": "United Kingdom",
            "claimed_by": "Argentina",
            "description": clean_text(text)
        }

    # Handle South Georgia and South Sandwich Islands
    if iso3Code == 'SGS':
        return {
            "type": "overseas_territory",
            "administered_by": "United Kingdom",
            "status": "uninhabited_territory",
            "description": clean_text(text) if text else "Uninhabited overseas territory"
        }

    # Handle Vatican
    if iso3Code == 'VAT':
        return {
            "type": "city_state",
            "description": "Sovereign city-state with no internal divisions"
        }

    # Handle very complex countries that need HTML parsing
    html_complex_codes = ['RUS', 'CHN', 'GBR',
                          'HUN', 'TWN', 'KOR', 'PRK', 'VNM', 'PHL']
    if iso3Code in html_complex_codes and ('<strong>' in text or '<p>' in text):
        # These will be handled by the HTML parsing logic in the main function
        return None

    # Handle countries with extremely long division lists
    long_list_codes = ['UGA', 'EST', 'SVN', 'ISL']
    if iso3Code in long_list_codes:
        # Use standard parsing but add metadata about length
        divisions = extract_divisions_from_text(text, iso3Code)
        if len(divisions) > 50:
            return {
                "type": "extensive_divisions",
                "divisions": divisions,
                "division_count": len(divisions),
                "note": f"Country has {len(divisions)} administrative divisions"
            }

    return None


def parse_admin_divisions(iso3Code: str, return_original: bool = False)-> dict:
    """
    Enhanced parser for administrative divisions from CIA JSON data

    Args:
        iso3Code: ISO3 country code

    Returns:
        Dict with comprehensive parsed administrative division data:
        {
            "admin_divisions": {...},
            "admin_divisions_note": str
        }
    """
    import logging
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

    logger = logging.getLogger(__name__)

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return {"admin_divisions": {}, "admin_divisions_note": ""}

    government_section = raw_data.get('Government', {})
    test_data = government_section.get('Administrative divisions', {})

    if return_original:
        return test_data


    # Handle empty input
    if not isinstance(test_data, dict) or not test_data:
        return {
            "admin_divisions": {},
            "admin_divisions_note": ""
        }

    try:
        text_data = test_data.get('text', '')
        note_data = test_data.get('note', '')

        if not text_data:
            return {
                "admin_divisions": {},
                "admin_divisions_note": clean_text(note_data) if note_data else ""
            }

        result = {
            "admin_divisions": {},
            "admin_divisions_note": ""
        }

        # Handle World data
        if iso3Code == 'WLD':
            result["admin_divisions"] = {
                "type": "global_summary",
                "summary": clean_text(text_data),
                "description": "Global administrative divisions overview"
            }
            if note_data:
                result["admin_divisions_note"] = clean_text(note_data)
            return result

        # Check for special cases first
        special_case = parse_special_cases(text_data, iso3Code)
        if special_case:
            result["admin_divisions"] = special_case
            if note_data:
                result["admin_divisions_note"] = clean_text(note_data)
            return result

        # Extract basic information
        clean_text_data = clean_text(text_data)
        division_count = extract_division_count(clean_text_data)

        # Check if this is HTML-formatted categorized data
        if ('<strong>' in text_data or '<p>' in text_data) and ':' in text_data:
            # Parse categorized divisions (like UK, China, Russia)
            categories = parse_html_categorized_divisions(text_data)

            if categories:
                # Calculate total count
                total_count = sum(cat.get('count', 0)
                                  for cat in categories.values())

                result["admin_divisions"] = {
                    "type": "categorized",
                    "categories": categories,
                    "total_categories": len(categories),
                    "total_divisions": total_count,
                    "division_count": division_count if division_count else total_count
                }
            else:
                # Fallback to simple parsing
                divisions = extract_divisions_from_text(clean_text_data)
                result["admin_divisions"] = {
                    "type": "simple_list",
                    "division_count": division_count or len(divisions),
                    "divisions": divisions
                }
        else:
            # Handle simple format
            divisions = extract_divisions_from_text(clean_text_data)

            # Extract administrative unit type
            unit_type = "divisions"  # default
            type_patterns = [
                r'(\d+)\s+(states?|provinces?|regions?|departments?|counties?|districts?|territories?|governorates?|municipalities?|cantons?|parishes?|oblasts?|voivodships?|prefectures?|boroughs?|councils?|communes?|emirates?|atolls?)',
                r'(\d+)\s+([^;,\(]+?)(?:\s*\([^)]*\))?\s*[;,:]'
            ]

            for pattern in type_patterns:
                match = re.search(pattern, clean_text_data, re.IGNORECASE)
                if match:
                    unit_type = match.group(2).strip().lower()
                    break

            # Extract territorial information
            territorial_info = extract_territorial_info(text_data)

            result["admin_divisions"] = {
                "type": "simple_list",
                "unit_type": unit_type,
                "division_count": division_count or len(divisions),
                "divisions": divisions
            }

            # Add territorial info if applicable
            if territorial_info["is_territory"]:
                result["admin_divisions"]["territorial_info"] = territorial_info

            # Extract special notes and administrative details
            special_notes = []

            # Look for note patterns in the text
            note_patterns = [
                r'note\s*[-:]?\s*([^;]+)',
                r';\s*note\s*[-:]?\s*([^;]+)',
                r'\([^)]*note[^)]*\)'
            ]

            for pattern in note_patterns:
                matches = re.findall(pattern, text_data, re.IGNORECASE)
                for match in matches:
                    clean_note = clean_text(match)
                    if len(clean_note) > 10:  # Avoid very short notes
                        special_notes.append(clean_note)

            if special_notes:
                result["admin_divisions"]["special_notes"] = special_notes

            # Handle countries with multiple administrative levels
            if ' and ' in clean_text_data and division_count:
                # Parse complex counts like "50 states and 1 district"
                and_match = re.search(
                    r'(\d+)\s+([^,;]+?)\s+and\s+(\d+)\s+([^,;]+)', clean_text_data)
                if and_match:
                    result["admin_divisions"]["composition"] = {
                        "primary": {
                            "count": int(and_match.group(1)),
                            "type": and_match.group(2).strip()
                        },
                        "secondary": {
                            "count": int(and_match.group(3)),
                            "type": and_match.group(4).strip()
                        }
                    }

        # Handle additional notes
        if note_data:
            result["admin_divisions_note"] = clean_text(note_data)

        # Add metadata
        result["admin_divisions"]["iso3_code"] = iso3Code
        result["admin_divisions"]["original_text"] = text_data

        return result

    except Exception as e:
        if app_logger:
            app_logger.error(
                f"Error parsing administrative divisions for {iso3Code}: {e}")
        return {
            "admin_divisions": {
                "type": "parse_error",
                "error": str(e),
                "iso3_code": iso3Code
            },
            "admin_divisions_note": ""
        }


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_admin_divisions")
    print("="*60)
    for iso3 in ['USA', 'FRA', 'DEU', 'GBR', 'CHN', 'IND']:
        print(f"\n{iso3}:")
        try:
            result = parse_admin_divisions(iso3)
            if result and result.get('admin_divisions'):
                ad = result['admin_divisions']
                print(f"  Type: {ad.get('type', 'N/A')}")
                print(f"  Count: {ad.get('division_count', 'N/A')}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
