######################################################################################################################
# CORE IMPORTS
# C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\c_00_transform_utils\extract_and_parse.py
# ---------------------------------------------------------------------------------------------------------------------
import inspect
from proj_004_cia.__logger.logger import app_logger
from typing import Dict, Any, List, Optional, Union, Tuple
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import iso3Code_to_cia_code


def _is_new_style_parser(parser_function) -> bool:
    """
    Detect if a parser function uses NEW style (data first) or OLD style (iso3Code first).

    NEW style: parse_X(data: dict, iso3Code: str = None, ...)
    OLD style: parse_X(iso3Code: str, return_original: bool = False, ...)

    Returns True if NEW style, False if OLD style.
    """
    try:
        sig = inspect.signature(parser_function)
        params = list(sig.parameters.values())

        if not params:
            return True  # Default to NEW style

        first_param = params[0]
        # Check if first parameter annotation is dict or if name suggests data
        if first_param.annotation == dict:
            return True
        if first_param.annotation == str or first_param.name == 'iso3Code':
            return False
        # Check by parameter name pattern
        if first_param.name.endswith('_data') or first_param.name == 'data':
            return True

        return True  # Default to NEW style
    except Exception:
        return True  # Default to NEW style on error

######################################################################################################################
# ENHANCED EXTRACT AND PARSE UTILITY
######################################################################################################################


def extract_and_parse(main_data: Dict[str, Any],
                      key_path: str,
                      parser_function,
                      iso3Code: str,
                      parser_name: str = "data",
                      is_world_data: bool = False,
                      allow_empty: bool = True,
                      default_value: Any = None) -> Any:
    """
    Enhanced helper function to extract and parse data with comprehensive error handling.

    Args:
        main_data: The main data dictionary
        key_path: Dot-separated path to the data (e.g., "Geography.Location")
        parser_function: Function to parse the extracted data
        iso3Code: Country ISO3 code
        parser_name: Name for logging purposes
        is_world_data: True if data is only available for World level
        allow_empty: Whether to allow empty/missing data
        default_value: Value to return if data is missing and allow_empty is False

    Returns:
        Parsed data or default value
    """
    try:
        # Handle World data restrictions
        if is_world_data and iso3Code != 'WLD':
            if app_logger:
                app_logger.debug(
                    f"Data for '{parser_name}' is World-only. Skipping for {iso3Code}")
            return default_value if default_value is not None else {}

        # Extract data using key path
        data = main_data
        path_parts = key_path.split('.')

        for i, key in enumerate(path_parts):
            if not isinstance(data, dict):
                if app_logger:
                    app_logger.warning(
                        f"Non-dict data at path step {i} for '{parser_name}' in {iso3Code}")
                return default_value if default_value is not None else {}

            data = data.get(key, {})

        # Check if data is empty
        if not data and not allow_empty:
            if app_logger:
                app_logger.warning(
                    f"Empty data for '{parser_name}' in {iso3Code} (not allowed)")
            return default_value if default_value is not None else {}

        if not data:
            return default_value if default_value is not None else {}

        # Parse the data
        try:
            # Detect parser style and call accordingly
            if _is_new_style_parser(parser_function):
                # NEW style: parse_X(data, iso3Code)
                parsed_result = parser_function(data, iso3Code)
            else:
                # OLD style: parse_X(iso3Code) - parser loads data internally
                # Note: OLD style parsers ignore the extracted data and reload it
                # This is a compatibility shim; parsers should be converted to NEW style
                parsed_result = parser_function(iso3Code)

            # Validate parsed result
            if parsed_result is None and not allow_empty:
                if app_logger:
                    app_logger.warning(
                        f"Parser returned None for '{parser_name}' in {iso3Code}")
                return default_value if default_value is not None else {}

            return parsed_result

        except Exception as e:
            country_info = iso3Code_to_cia_code().get(iso3Code, {})
            if app_logger:
                app_logger.error(f"Parser error in '{parser_function.__name__}' for {parser_name} "
                                 f"in {iso3Code} ({country_info.get('country_name', 'Unknown')}): {e}")
            return default_value if default_value is not None else {}

    except Exception as e:
        country_info = iso3Code_to_cia_code().get(iso3Code, {})
        if app_logger:
            app_logger.error(f"Extraction error for '{parser_name}' "
                             f"in {iso3Code} ({country_info.get('country_name', 'Unknown')}): {e}")
        return default_value if default_value is not None else {}
