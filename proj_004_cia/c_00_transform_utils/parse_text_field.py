######################################################################################################################
# CORE IMPORTS
# C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\c_00_transform_utils\parse_text_field.py

# ---------------------------------------------------------------------------------------------------------------------
from proj_004_cia.__logger.logger import app_logger
from typing import Dict, Any, List, Optional, Union, Tuple
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
# ----------------------------------------------------------------------------------------------------------------------


######################################################################################################################
# ENHANCED TEXT FIELD PARSING
######################################################################################################################

def parse_text_field(data: Dict[str, Any],
                     key_name: str,
                     iso3Code: str = "",
                     required: bool = False,
                     default_value: str = "") -> str:
    """
    Enhanced text field parsing with validation and error handling.

    Args:
        data: Dictionary to extract text from
        key_name: Name of the field for logging
        iso3Code: Country code for logging
        required: Whether the field is required
        default_value: Default value if field is missing

    Returns:
        Cleaned text or default value
    """
    if not isinstance(data, dict):
        if required and app_logger:
            app_logger.error(
                f"Required field '{key_name}' missing for {iso3Code}: data is not a dict")
        return default_value

    try:
        text = data.get('text', '')

        if not text or not isinstance(text, str):
            if required and app_logger:
                app_logger.warning(
                    f"Required field '{key_name}' missing or empty for {iso3Code}")
            return default_value

        cleaned = clean_text(text)

        if not cleaned and required and app_logger:
            app_logger.warning(
                f"Required field '{key_name}' is empty after cleaning for {iso3Code}")

        return cleaned if cleaned else default_value

    except Exception as e:
        if app_logger:
            app_logger.error(
                f"Error parsing text field '{key_name}' for {iso3Code}: {e}")
        return default_value
