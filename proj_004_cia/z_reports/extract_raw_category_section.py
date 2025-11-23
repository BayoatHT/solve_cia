"""
Extract Raw Category Section Data

Extracts raw CIA World Factbook data for a specific category and section
across all countries. Outputs a Python dictionary file with ISO3 codes as keys.

Usage:
    python extract_raw_category_section.py <category> <section>
    python extract_raw_category_section.py "Environment" "Major rivers (by length in km)"
    python extract_raw_category_section.py "Economy" "GDP (official exchange rate)"

Output:
    Creates a file in _reports/ named: raw_<category>_<section>.py
"""

import os
import sys
import json
import re
from datetime import datetime
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data, ISO3_TO_CIA


def sanitize_filename(name: str) -> str:
    """Convert a string to a valid filename."""
    # Replace spaces and special chars with underscores
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s-]+', '_', name)
    return name.lower().strip('_')


def get_available_categories() -> Dict[str, list]:
    """Get all available categories and their sections from sample country."""
    data = load_country_data('USA')
    categories = {}
    for cat_name, cat_data in data.items():
        if isinstance(cat_data, dict):
            categories[cat_name] = list(cat_data.keys())
    return categories


def extract_raw_section(category: str, section: str) -> Dict[str, Any]:
    """
    Extract raw data for a specific category/section from all countries.

    Args:
        category: Category name (e.g., "Environment", "Economy")
        section: Section name within the category (e.g., "Climate", "GDP")

    Returns:
        Dictionary with ISO3 codes as keys and raw section data as values
    """
    results = {}
    errors = []

    for iso3Code in ISO3_TO_CIA.keys():
        try:
            data = load_country_data(iso3Code)
            cat_data = data.get(category, {})
            section_data = cat_data.get(section, None)

            if section_data is not None:
                results[iso3Code] = section_data
            else:
                results[iso3Code] = None

        except Exception as e:
            errors.append(f"{iso3Code}: {str(e)}")
            results[iso3Code] = None

    return results, errors


def save_report(data: Dict[str, Any], category: str, section: str, output_dir: str) -> str:
    """
    Save extracted data to a Python file in _reports directory.

    Args:
        data: Dictionary of extracted data
        category: Category name
        section: Section name
        output_dir: Directory to save the report

    Returns:
        Path to the saved file
    """
    # Generate filename
    cat_safe = sanitize_filename(category)
    sec_safe = sanitize_filename(section)
    filename = f"raw_{cat_safe}_{sec_safe}.py"
    filepath = os.path.join(output_dir, filename)

    # Count non-null entries
    non_null = sum(1 for v in data.values() if v is not None)

    # Generate Python file content
    content = f'''"""
Raw Data Report: {category} > {section}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Countries with data: {non_null} / {len(data)}

This file contains raw CIA World Factbook data for the specified section
across all countries. Each key is an ISO3 country code.
"""

RAW_DATA = {json.dumps(data, indent=4, ensure_ascii=False)}
'''

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath


def list_categories():
    """Print all available categories and sections."""
    categories = get_available_categories()
    print("\nAvailable Categories and Sections:")
    print("=" * 60)
    for cat, sections in sorted(categories.items()):
        print(f"\n{cat}:")
        for sec in sections:
            print(f"    - {sec}")


def main():
    # Get script directory for output
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "_reports")
    os.makedirs(output_dir, exist_ok=True)

    # Parse arguments
    if len(sys.argv) < 3:
        print("Usage: python extract_raw_category_section.py <category> <section>")
        print("\nExamples:")
        print('  python extract_raw_category_section.py "Environment" "Climate"')
        print('  python extract_raw_category_section.py "Economy" "Real GDP growth rate"')
        print("\nUse --list to see all available categories and sections")

        if len(sys.argv) == 2 and sys.argv[1] == "--list":
            list_categories()
        sys.exit(1)

    category = sys.argv[1]
    section = sys.argv[2]

    print(f"Extracting raw data for: {category} > {section}")
    print("-" * 60)

    # Validate category/section exist
    categories = get_available_categories()
    if category not in categories:
        print(f"Error: Category '{category}' not found.")
        print(f"Available categories: {', '.join(categories.keys())}")
        sys.exit(1)

    if section not in categories[category]:
        print(f"Error: Section '{section}' not found in category '{category}'.")
        print(f"Available sections: {', '.join(categories[category])}")
        sys.exit(1)

    # Extract data
    data, errors = extract_raw_section(category, section)

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
