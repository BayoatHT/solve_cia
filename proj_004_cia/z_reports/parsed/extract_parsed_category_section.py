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

from proj_004_cia.z_reports.category_sections import (
    PARSED_CATEGORIES,
    CATEGORY_PARSERS,
    get_parsed_sections,
    get_parser,
    list_all_parsed
)
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data, ISO3_TO_CIA
import os
import sys
import json
import re
from datetime import datetime
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))


def sanitize_filename(name: str) -> str:
    """Convert a string to a valid filename."""
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s-]+', '_', name)
    return name.lower().strip('_')


def extract_parsed_section(category: str, section: Optional[str] = None) -> tuple:
    """
    Extract parsed data for a specific category/section from all countries.

    Args:
        category: Category name (e.g., "Environment", "Economy")
        section: Optional section key to filter (e.g., "major_rivers", "climate")

    Returns:
        Tuple of (results dict, errors list)
    """
    parser = get_parser(category)
    if parser is None:
        raise ValueError(f"Unknown category: {category}")

    results = {}
    errors = []

    for iso3Code in ISO3_TO_CIA.keys():
        try:
            data = load_country_data(iso3Code)
            parsed = parser(data, iso3Code)

            if section and isinstance(parsed, dict):
                results[iso3Code] = parsed.get(section, None)
            else:
                results[iso3Code] = parsed

        except Exception as e:
            errors.append(f"{iso3Code}: {str(e)}")
            results[iso3Code] = None

    return results, errors


def to_python_format(data: Any) -> str:
    """Convert data to Python-friendly string format (None instead of null, etc.)."""
    json_str = json.dumps(data, indent=4, ensure_ascii=False, default=str)
    # Convert JSON syntax to Python syntax
    json_str = json_str.replace(': null', ': None')
    json_str = json_str.replace(': true', ': True')
    json_str = json_str.replace(': false', ': False')
    return json_str


def save_report(data: Dict[str, Any], category: str, section: Optional[str], output_dir: str) -> str:
    """Save extracted data to a Python file in _reports directory."""
    cat_safe = sanitize_filename(category)
    sec_safe = sanitize_filename(section) if section else "all"
    filename = f"parsed_{cat_safe}_{sec_safe}.py"
    filepath = os.path.join(output_dir, filename)

    non_null = sum(1 for v in data.values() if v is not None)
    section_desc = f" > {section}" if section else " (all sections)"

    content = f'''"""
Parsed Data Report: {category}{section_desc}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Countries with data: {non_null} / {len(data)}

This file contains parsed/processed CIA World Factbook data for the specified
category and section across all countries. Each key is an ISO3 country code.
"""

PARSED_DATA = {to_python_format(data)}
'''

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath


def run_extraction(category: str, section: Optional[str] = None, output_dir: str = None) -> Dict[str, Any]:
    """
    Run extraction for a category/section and save report.

    Args:
        category: Category name
        section: Optional section name (None for all sections)
        output_dir: Output directory (defaults to _reports/)

    Returns:
        Dictionary of extracted data
    """
    if output_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "_reports")
    os.makedirs(output_dir, exist_ok=True)

    # Validate category
    if category not in CATEGORY_PARSERS:
        raise ValueError(
            f"Unknown category: {category}. Available: {list(CATEGORY_PARSERS.keys())}")

    # Validate section if provided
    if section:
        available_sections = get_parsed_sections(category)
        if section not in available_sections:
            print(
                f"Warning: Section '{section}' may not exist. Available: {available_sections}")

    section_desc = f" > {section}" if section else ""
    print(f"Extracting parsed data for: {category}{section_desc}")
    print("-" * 60)

    data, errors = extract_parsed_section(category, section)
    filepath = save_report(data, category, section, output_dir)

    non_null = sum(1 for v in data.values() if v is not None)
    print(f"Countries processed: {len(data)}")
    print(f"Countries with data: {non_null}")
    print(f"Countries without data: {len(data) - non_null}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for err in errors[:5]:
            print(f"  - {err}")

    print(f"\nReport saved to: {filepath}")
    return data


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python extract_parsed_category_section.py <category> [section]")
        print("\nExamples:")
        print('  python extract_parsed_category_section.py "Environment"')
        print('  python extract_parsed_category_section.py "Environment" "major_rivers"')
        print('  python extract_parsed_category_section.py "Economy" "gdp"')
        print("\nUse --list to see all available categories and sections")
        sys.exit(1)

    if sys.argv[1] == "--list":
        list_all_parsed()
        sys.exit(0)

    category = sys.argv[1]
    section = sys.argv[2] if len(sys.argv) > 2 else None
    run_extraction(category, section)


######################################################################################################################
#   TEST CONFIGURATION - Change these values to test different extractions
######################################################################################################################
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # Configure test extraction here:
    TEST_CATEGORY = "Geography"
    TEST_SECTION = "elevation"  # Set to None to extract all sections
    # --------------------------------------------------------------------------------------------------

    # If command line args provided, use main(), otherwise use test config
    if len(sys.argv) > 1:
        main()
    else:
        print("Running with test configuration...")
        print(f"Category: {TEST_CATEGORY}")
        print(f"Section: {TEST_SECTION}")
        print()
        run_extraction(TEST_CATEGORY, TEST_SECTION)
