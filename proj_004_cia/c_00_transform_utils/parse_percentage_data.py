
######################################################################################################################
# CORE IMPORTS
# C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\c_00_transform_utils\parse_percentage_data.py
# ---------------------------------------------------------------------------------------------------------------------
import re
from proj_004_cia.__logger.logger import app_logger
from typing import Dict, Any, List, Optional, Union, Tuple
# ---------------------------------------------------------------------------------------------------------------------

######################################################################################################################
# ENHANCED PERCENTAGE PARSING
######################################################################################################################


def parse_percentage_data(data_string: str,
                          iso3Code: str = "",
                          return_decimal: bool = True,
                          extract_year: bool = True) -> dict:
    """
    Enhanced percentage parsing with support for various formats.

    Args:
        data_string: String containing percentage data
        iso3Code: Country code for logging
        return_decimal: Whether to return percentage as decimal (0.15) or percent (15)
        extract_year: Whether to extract year information

    Returns:
        Dictionary with percentage and metadata

    Examples:
        >>> parse_percentage_data("15.2% (2023 est.)")
        {"value": 0.152, "year": 2023, "is_estimate": True}
    """
    if not isinstance(data_string, str) or not data_string.strip():
        return {}

    try:
        text = data_string.strip()
        result = {}

        # Enhanced percentage extraction patterns
        percentage_patterns = [
            r'([\d.]+)%\s*\((\d{4})\s*est\.?\)',        # 15.2% (2023 est.)
            r'([\d.]+)%\s*\((\d{4})\)',                 # 15.2% (2023)
            r'([\d.]+)\s*percent\s*\((\d{4})\)',        # 15.2 percent (2023)
            r'([\d.]+)%',                               # 15.2%
            r'([\d.]+)\s*percent',                      # 15.2 percent
        ]

        percentage_value = None
        year_value = None
        is_estimate = False

        for pattern in percentage_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                percentage_value = float(match.group(1))

                if len(match.groups()) > 1:
                    year_value = int(match.group(2))

                if 'est' in text.lower():
                    is_estimate = True

                break

        if percentage_value is None:
            # Try to extract just a number and assume it's a percentage
            number_match = re.search(r'([\d.]+)', text)
            if number_match:
                percentage_value = float(number_match.group(1))
            else:
                raise ValueError(f"No percentage value found in: {text}")

        # Convert to decimal if requested
        if return_decimal:
            result['value'] = percentage_value / 100
            result['percentage'] = percentage_value
        else:
            result['value'] = percentage_value

        # Add metadata
        if extract_year and year_value:
            result['year'] = year_value

        result['is_estimate'] = is_estimate
        result['original_text'] = data_string

        # Extract additional context
        if 'annual' in text.lower():
            result['period'] = 'annual'
        elif 'monthly' in text.lower():
            result['period'] = 'monthly'

        return result

    except Exception as e:
        if app_logger:
            app_logger.error(
                f"Error parsing percentage data '{data_string}' for {iso3Code}: {e}")
        return {}
