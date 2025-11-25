"""
Base utilities for extracting string/scalar features from country data.

This module provides helper functions to extract single-value string fields
across all countries in a consistent format.
"""

from typing import Dict, Callable, Optional, Any
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import ISO3_TO_CIA, load_country_data


def extract_string_feature(
    parser_func: Callable,
    extractor_func: Callable[[Dict], Optional[str]],
    feature_name: str,
    verbose: bool = False
) -> Dict[str, str]:
    """
    Extract a string feature for all countries.

    Args:
        parser_func: Function to parse raw country data (e.g., return_geography_data)
        extractor_func: Function to extract string from parsed data
        feature_name: Name of the feature for logging
        verbose: Whether to print progress

    Returns:
        Dictionary mapping ISO3 codes to string values

    Example:
        >>> def extract_capital(parsed_data):
        ...     return parsed_data.get('capital_name', '')
        >>>
        >>> from proj_004_cia.c_05_government.return_government_data import return_government_data
        >>> capitals = extract_string_feature(
        ...     return_government_data,
        ...     extract_capital,
        ...     'capital'
        ... )
    """
    results = {}
    success_count = 0
    empty_count = 0
    error_count = 0

    for iso3Code in sorted(ISO3_TO_CIA.keys()):
        try:
            # Load raw country data
            raw_data = load_country_data(iso3Code)

            # Parse the data
            parsed_data = parser_func(raw_data, iso3Code)

            # Extract the string value
            string_value = extractor_func(parsed_data)

            if string_value and isinstance(string_value, str):
                results[iso3Code] = string_value.strip()
                success_count += 1
            else:
                empty_count += 1

        except Exception as e:
            if verbose:
                print(f"Error processing {iso3Code}: {e}")
            error_count += 1

    if verbose:
        total = len(ISO3_TO_CIA)
        coverage = (success_count / total * 100) if total > 0 else 0
        print(f"\n=== {feature_name} Extraction Summary ===")
        print(f"Total countries: {total}")
        print(f"Successfully extracted: {success_count} ({coverage:.1f}%)")
        print(f"Empty/None values: {empty_count}")
        print(f"Errors: {error_count}")

    return results


def extract_text_field(data: Dict, field_name: str) -> Optional[str]:
    """
    Extract a text field from parsed data dictionary.

    Args:
        data: Parsed country data dictionary
        field_name: Name of the field to extract

    Returns:
        String value or None if not found/empty
    """
    value = data.get(field_name)

    if isinstance(value, str) and value.strip():
        return value.strip()

    return None


def extract_nested_text(data: Dict, *keys) -> Optional[str]:
    """
    Extract text from nested dictionary structure.

    Args:
        data: Parsed country data dictionary
        *keys: Sequence of keys to traverse

    Returns:
        String value or None if not found

    Example:
        >>> extract_nested_text(data, 'capital', 'name')
    """
    current = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        else:
            return None

    if isinstance(current, str) and current.strip():
        return current.strip()

    return None
