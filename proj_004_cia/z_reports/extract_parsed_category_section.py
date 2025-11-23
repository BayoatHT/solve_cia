"""
Extract Parsed Category Section Data

Extracts parsed/processed CIA World Factbook data for a specific category
and optionally a specific section across all countries.

Uses the return_*_data() functions to get fully parsed data.

Usage:
    python extract_parsed_category_section.py <category> [section]
    python extract_parsed_category_section.py "Environment"
    python extract_parsed_category_section.py "Environment" "major_rivers"
    python extract_parsed_category_section.py "Economy" "gdp"

Output:
    Creates a file in _reports/ named: parsed_<category>_<section>.py
"""

import os
import sys
import json
import re
from datetime import datetime
from typing import Dict, Any, Optional, Callable

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data, ISO3_TO_CIA

# Import all return_*_data functions
from proj_004_cia.c_01_intoduction.return_introduction_data import return_introduction_data
from proj_004_cia.c_02_geography.return_geography_data import return_geography_data
from proj_004_cia.c_03_society.return_society_data import return_society_data
from proj_004_cia.c_04_environment.return_environment_data import return_environment_data
from proj_004_cia.c_05_government.return_government_data import return_government_data
from proj_004_cia.c_06_economy.return_economy_data import return_economy_data
from proj_004_cia.c_07_energy.return_energy_data import return_energy_data
from proj_004_cia.c_08_communications.return_communications_data import return_communications_data
from proj_004_cia.c_09_transportation.return_transportation_data import return_transportation_data
from proj_004_cia.c_10_military.return_military_data import return_military_data
from proj_004_cia.c_11_space.return_space_data import return_space_data
from proj_004_cia.c_12_terrorism.return_terrorism_data import return_terrorism_data
from proj_004_cia.c_13_issues.return_issues_data import return_issues_data


# Map raw category names to parser functions
CATEGORY_PARSERS: Dict[str, Callable] = {
    'Introduction': return_introduction_data,
    'Geography': return_geography_data,
    'People and Society': return_society_data,
    'Environment': return_environment_data,
    'Government': return_government_data,
    'Economy': return_economy_data,
    'Energy': return_energy_data,
    'Communications': return_communications_data,
    'Transportation': return_transportation_data,
    'Military and Security': return_military_data,
    'Space': return_space_data,
    'Terrorism': return_terrorism_data,
    'Transnational Issues': return_issues_data,
}


def sanitize_filename(name: str) -> str:
    """Convert a string to a valid filename."""
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s-]+', '_', name)
    return name.lower().strip('_')


def get_available_sections(category: str) -> list:
    """Get available parsed sections for a category by checking sample output."""
    if category not in CATEGORY_PARSERS:
        return []

    parser = CATEGORY_PARSERS[category]
    try:
        data = load_country_data('USA')
        result = parser(data, 'USA')
        if isinstance(result, dict):
            return list(result.keys())
    except Exception:
        pass
    return []


def extract_parsed_section(category: str, section: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract parsed data for a specific category/section from all countries.

    Args:
        category: Category name (e.g., "Environment", "Economy")
        section: Optional section key to filter (e.g., "major_rivers", "climate")

    Returns:
        Dictionary with ISO3 codes as keys and parsed data as values
    """
    if category not in CATEGORY_PARSERS:
        raise ValueError(f"Unknown category: {category}")

    parser = CATEGORY_PARSERS[category]
    results = {}
    errors = []

    for iso3Code in ISO3_TO_CIA.keys():
        try:
            data = load_country_data(iso3Code)
            parsed = parser(data, iso3Code)

            if section and isinstance(parsed, dict):
                # Filter to specific section
                results[iso3Code] = parsed.get(section, None)
            else:
                results[iso3Code] = parsed

        except Exception as e:
            errors.append(f"{iso3Code}: {str(e)}")
            results[iso3Code] = None

    return results, errors


def save_report(data: Dict[str, Any], category: str, section: Optional[str], output_dir: str) -> str:
    """
    Save extracted data to a Python file in _reports directory.
    """
    cat_safe = sanitize_filename(category)
    sec_safe = sanitize_filename(section) if section else "all"
    filename = f"parsed_{cat_safe}_{sec_safe}.py"
    filepath = os.path.join(output_dir, filename)

    # Count non-null entries
    non_null = sum(1 for v in data.values() if v is not None)

    section_desc = f" > {section}" if section else " (all sections)"

    content = f'''"""
Parsed Data Report: {category}{section_desc}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Countries with data: {non_null} / {len(data)}

This file contains parsed/processed CIA World Factbook data for the specified
category and section across all countries. Each key is an ISO3 country code.
"""

PARSED_DATA = {json.dumps(data, indent=4, ensure_ascii=False, default=str)}
'''

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath


def list_categories():
    """Print all available categories and their parsed sections."""
    print("\nAvailable Categories and Parsed Sections:")
    print("=" * 60)
    for cat in sorted(CATEGORY_PARSERS.keys()):
        sections = get_available_sections(cat)
        print(f"\n{cat}:")
        for sec in sections:
            print(f"    - {sec}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "_reports")
    os.makedirs(output_dir, exist_ok=True)

    if len(sys.argv) < 2:
        print("Usage: python extract_parsed_category_section.py <category> [section]")
        print("\nExamples:")
        print('  python extract_parsed_category_section.py "Environment"')
        print('  python extract_parsed_category_section.py "Environment" "major_rivers"')
        print('  python extract_parsed_category_section.py "Economy" "gdp"')
        print("\nUse --list to see all available categories and sections")
        sys.exit(1)

    if sys.argv[1] == "--list":
        list_categories()
        sys.exit(0)

    category = sys.argv[1]
    section = sys.argv[2] if len(sys.argv) > 2 else None

    if category not in CATEGORY_PARSERS:
        print(f"Error: Category '{category}' not found.")
        print(f"Available categories: {', '.join(CATEGORY_PARSERS.keys())}")
        sys.exit(1)

    # Validate section if provided
    if section:
        available_sections = get_available_sections(category)
        if section not in available_sections:
            print(f"Warning: Section '{section}' may not exist in parsed output.")
            print(f"Available sections: {', '.join(available_sections)}")

    section_desc = f" > {section}" if section else ""
    print(f"Extracting parsed data for: {category}{section_desc}")
    print("-" * 60)

    # Extract data
    data, errors = extract_parsed_section(category, section)

    # Save report
    filepath = save_report(data, category, section, output_dir)

    # Summary
    non_null = sum(1 for v in data.values() if v is not None)
    print(f"Countries processed: {len(data)}")
    print(f"Countries with data: {non_null}")
    print(f"Countries without data: {len(data) - non_null}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for err in errors[:5]:
            print(f"  - {err}")
        if len(errors) > 5:
            print(f"  ... and {len(errors) - 5} more")

    print(f"\nReport saved to: {filepath}")


if __name__ == "__main__":
    main()
