######################################################################################################################
# CORE IMPORTS
# C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\c_00_transform_utils\extract_numeric_value.py
# ---------------------------------------------------------------------------------------------------------------------
import re
from proj_004_cia.__logger.logger import app_logger
from typing import Dict, Any, List, Optional, Union, Tuple
# ---------------------------------------------------------------------------------------------------------------------

######################################################################################################################
# ENHANCED NUMERIC VALUE EXTRACTION
######################################################################################################################


def extract_numeric_value(text: str,
                          unit: str = None,
                          iso3Code: str = "",
                          allow_ranges: bool = True,
                          return_metadata: bool = False) -> Union[float, Dict[str, Any], None]:
    """
    Enhanced numeric value extraction with support for ranges, units, and metadata.

    Args:
        text: Text containing numeric value
        unit: Expected unit (optional)
        iso3Code: Country code for logging
        allow_ranges: Whether to handle range values (e.g., "15-25")
        return_metadata: Whether to return additional metadata

    Returns:
        Numeric value, range dict, or metadata dict

    Examples:
        >>> extract_numeric_value("123.45 sq km")
        123.45

        >>> extract_numeric_value("15-25 years", allow_ranges=True, return_metadata=True)
        {"value": 20.0, "min": 15.0, "max": 25.0, "unit": "years", "is_range": True}
    """
    if not text or not isinstance(text, str):
        return None

    try:
        original_text = text.strip()
        working_text = original_text.lower()

        # Handle special cases
        special_values = {
            'na': None, 'n/a': None, 'not available': None,
            'negligible': 0, 'trace': 0.001, 'less than 1': 0.5
        }

        if working_text in special_values:
            return special_values[working_text]

        # Remove unit if specified
        if unit:
            unit_lower = unit.lower()
            if unit_lower in working_text:
                working_text = working_text.replace(unit_lower, '').strip()

        # Handle magnitude modifiers
        magnitude_multipliers = {
            'thousand': 1_000, 'k': 1_000,
            'million': 1_000_000, 'm': 1_000_000, 'mn': 1_000_000,
            'billion': 1_000_000_000, 'b': 1_000_000_000, 'bn': 1_000_000_000,
            'trillion': 1_000_000_000_000, 't': 1_000_000_000_000, 'tn': 1_000_000_000_000
        }

        multiplier = 1
        for magnitude, mult_value in magnitude_multipliers.items():
            if magnitude in working_text:
                multiplier = mult_value
                working_text = working_text.replace(magnitude, '').strip()
                break

        # Extract numeric patterns
        # Handle ranges (e.g., "15-25", "10 to 20")
        range_patterns = [
            r'(\d+(?:\.\d+)?)\s*[-–—]\s*(\d+(?:\.\d+)?)',  # 15-25 or 15–25
            r'(\d+(?:\.\d+)?)\s+to\s+(\d+(?:\.\d+)?)',      # 15 to 25
            # between 15 and 25
            r'between\s+(\d+(?:\.\d+)?)\s+and\s+(\d+(?:\.\d+)?)'
        ]

        if allow_ranges:
            for pattern in range_patterns:
                match = re.search(pattern, working_text)
                if match:
                    min_val = float(match.group(1)) * multiplier
                    max_val = float(match.group(2)) * multiplier
                    avg_val = (min_val + max_val) / 2

                    if return_metadata:
                        return {
                            "value": avg_val,
                            "min": min_val,
                            "max": max_val,
                            "unit": unit,
                            "is_range": True,
                            "original_text": original_text
                        }
                    return avg_val

        # Extract single numeric value
        numeric_pattern = r'(\d+(?:,\d{3})*(?:\.\d+)?)'
        match = re.search(numeric_pattern, working_text.replace(',', ''))

        if match:
            value = float(match.group(1).replace(',', '')) * multiplier

            if return_metadata:
                return {
                    "value": value,
                    "unit": unit,
                    "is_range": False,
                    "multiplier": multiplier,
                    "original_text": original_text
                }
            return value

        # If no numeric value found
        if app_logger:
            app_logger.warning(
                f"No numeric value found in '{original_text}' for {iso3Code}")
        return None

    except Exception as e:
        if app_logger:
            app_logger.error(
                f"Error extracting numeric value from '{text}' for {iso3Code}: {e}")
        return None
