######################################################################################################################
# CORE IMPORTS
# C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\c_00_transform_utils\parse_text_and_note.py
# ---------------------------------------------------------------------------------------------------------------------
from proj_004_cia.__logger.logger import app_logger
from typing import Dict, Any, List, Optional, Union, Tuple
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.parse_territorial_subdivisions import parse_territorial_subdivisions
# ----------------------------------------------------------------------------------------------------------------------

######################################################################################################################
# ENHANCED TEXT AND NOTE PARSING
######################################################################################################################


def parse_text_and_note(data: Dict[str, Any],
                        main_key: str,
                        iso3Code: str = "",
                        preserve_structure: bool = False) -> Dict[str, Any]:
    """
    Enhanced text and note parsing with territorial subdivision support.

    Args:
        data: Dictionary containing text and note fields
        main_key: Main key for the result
        iso3Code: Country code for logging
        preserve_structure: Whether to preserve territorial subdivisions

    Returns:
        Dictionary with cleaned text and note data
    """
    if not isinstance(data, dict):
        return {}

    try:
        result = {}
        main_key_lower = main_key.lower()

        # Extract and process text field
        text_data = data.get('text', '')
        if text_data and isinstance(text_data, str):
            # Check for territorial subdivisions (marked with <em> tags)
            if preserve_structure and '<em>' in text_data:
                territories = parse_territorial_subdivisions(text_data)
                if territories:
                    result[main_key_lower] = territories
                else:
                    result[main_key_lower] = clean_text(text_data)
            else:
                result[main_key_lower] = clean_text(text_data)
        else:
            result[main_key_lower] = ""

        # Extract and process note field
        note_data = data.get('note', '')
        if note_data and isinstance(note_data, str):
            result[f"{main_key_lower}_note"] = clean_text(note_data)
        else:
            result[f"{main_key_lower}_note"] = ""

        return result

    except Exception as e:
        if app_logger:
            app_logger.error(
                f"Error parsing text and note for '{main_key}' in {iso3Code}: {e}")
        return {main_key.lower(): "", f"{main_key.lower()}_note": ""}
