import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_major_lakes(iso3Code: str, return_original: bool = False)-> dict:
    """Parse major lakes from CIA Environment section for a given country."""
    result = {
        "major_lakes": {
            "fresh_water": [],
            "salt_water": [],
            "raw_text": None
        },
        "major_lakes_note": ""
    }

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    environment_section = raw_data.get('Environment', {})
    lakes_data = environment_section.get('Major lakes (area sq km)', {})

    if return_original:
        return lakes_data


    if not lakes_data or not isinstance(lakes_data, dict):
        return result

    def parse_lake_list(text, return_original: bool = False):
        """Parse lakes from various text formats."""
        if return_original:
            return text

        lakes = []
        if not text:
            return lakes, ""

        # Extract note if present
        note = ""
        note_match = re.search(r'note\s*[-–:]\s*(.+?)(?:$)', text, re.IGNORECASE)
        if note_match:
            note = note_match.group(1).strip()

        # Split by semicolons, handling entries that may contain notes
        entries = re.split(r';\s*', text)

        for entry in entries:
            # Skip notes and empty entries
            if not entry or entry.lower().startswith('note'):
                continue

            # Skip entries with non-numeric values like "largely dried up"
            if not re.search(r'\d', entry):
                continue

            # Pattern 1: Standard format with dash - "Name - NUMBER sq km" or "Name - MIN-MAX sq km"
            match = re.search(r'^(.+?)\s*[-–]\s*([\d,]+(?:\s*[-–]\s*[\d,]+)?)\s*sq\s*km', entry.strip(), re.IGNORECASE)

            # Pattern 2: Missing "sq km" - "Name - NUMBER"
            if not match:
                match = re.search(r'^(.+?)\s*[-–]\s*([\d,]+)\s*$', entry.strip())

            # Pattern 3: No dash - "Name NUMBER sq km" (like "Biwa-ko 688 sq km")
            if not match:
                match = re.search(r'^(.+?)\s+([\d,]+)\s*sq\s*km', entry.strip(), re.IGNORECASE)
            if match:
                raw_name = match.group(1).strip()
                area_str = match.group(2)

                # Parse area - handle ranges like "10,360-25,900"
                area_parts = re.findall(r'[\d,]+', area_str)
                if len(area_parts) >= 2:
                    area_min = int(area_parts[0].replace(',', ''))
                    area_max = int(area_parts[1].replace(',', ''))
                    area = None  # Use range instead
                elif area_parts:
                    area = int(area_parts[0].replace(',', ''))
                    area_min = None
                    area_max = None
                else:
                    continue

                # Extract shared info - handle both "shared with X" and "endorheic lake shared with X"
                shared_with = []
                shared_match = re.search(r'shared with\s+([^)]+)', raw_name, re.IGNORECASE)
                if shared_match:
                    shared_text = shared_match.group(1)
                    # Parse countries - handle "X and Y", "X, Y, and Z", "X, Y"
                    # Replace " and " with comma for uniform splitting
                    shared_text = re.sub(r'\s+and\s+', ', ', shared_text)
                    countries = [c.strip() for c in shared_text.split(',') if c.strip()]
                    shared_with = countries

                # Check for ephemeral flag
                is_ephemeral = 'ephemeral' in raw_name.lower()

                # Clean name - remove annotations but keep "Lake" prefix if present
                name = re.sub(r'\s*\([^)]*\)\s*', ' ', raw_name).strip()
                name = name.rstrip('*').strip()

                if name:
                    lake_data = {'name': name}

                    if area is not None:
                        lake_data['area_sq_km'] = area
                    else:
                        lake_data['area_sq_km_min'] = area_min
                        lake_data['area_sq_km_max'] = area_max

                    if shared_with:
                        lake_data['shared_with'] = shared_with
                    if is_ephemeral:
                        lake_data['is_ephemeral'] = True

                    lakes.append(lake_data)

        return lakes, note

    # Parse fresh water lakes
    fresh = lakes_data.get('fresh water lake(s)', {})
    if fresh and isinstance(fresh, dict):
        text = fresh.get('text', '')
        if text and text.upper() != 'NA':
            cleaned = clean_text(text)
            lakes, note = parse_lake_list(cleaned)
            result['major_lakes']['fresh_water'] = lakes
            if note:
                result['major_lakes_note'] = note
            if not result['major_lakes']['raw_text']:
                result['major_lakes']['raw_text'] = cleaned

    # Parse salt water lakes
    salt = lakes_data.get('salt water lake(s)', {})
    if salt and isinstance(salt, dict):
        text = salt.get('text', '')
        if text and text.upper() != 'NA':
            cleaned = clean_text(text)
            lakes, note = parse_lake_list(cleaned)
            result['major_lakes']['salt_water'] = lakes
            if note and not result['major_lakes_note']:
                result['major_lakes_note'] = note
            # Append to raw_text if fresh water already set it
            if result['major_lakes']['raw_text']:
                result['major_lakes']['raw_text'] += "; " + cleaned
            else:
                result['major_lakes']['raw_text'] = cleaned

    return result


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_major_lakes")
    print("="*60)
    for iso3 in ['USA', 'CAN', 'RUS', 'CHN', 'AUS', 'BRA']:
        print(f"\n{iso3}:")
        try:
            result = parse_major_lakes(iso3)
            if result and (result['major_lakes']['fresh_water'] or result['major_lakes']['salt_water']):
                ml = result['major_lakes']
                print(f"  Fresh water: {len(ml['fresh_water'])} lakes")
                for lake in ml['fresh_water'][:2]:
                    area = lake.get('area_sq_km', f"{lake.get('area_sq_km_min')}-{lake.get('area_sq_km_max')}")
                    print(f"    - {lake['name']}: {area} sq km")
                print(f"  Salt water: {len(ml['salt_water'])} lakes")
            else:
                print("  No lakes data")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
