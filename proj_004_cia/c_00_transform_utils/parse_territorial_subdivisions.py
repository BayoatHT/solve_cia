
######################################################################################################################
# CORE IMPORTS
# C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\c_00_transform_utils\parse_territorial_subdivisions.py
# ---------------------------------------------------------------------------------------------------------------------
import re
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from typing import Dict, Any
# ---------------------------------------------------------------------------------------------------------------------

######################################################################################################################
# NEW UTILITY: TERRITORIAL SUBDIVISION PARSING
######################################################################################################################


def parse_territorial_subdivisions(text: str) -> Dict[str, str]:
    """
    Parse territorial subdivisions marked with <em> tags.

    Args:
        text: Text containing territorial subdivisions

    Returns:
        Dictionary with territory names as keys and descriptions as values

    Examples:
        >>> parse_territorial_subdivisions("<em>mainland:</em> oil, gas; <em>islands:</em> fish")
        {"mainland": "oil, gas", "islands": "fish"}
    """
    if not isinstance(text, str) or '<em>' not in text:
        return {}

    try:
        territories = {}

        # Pattern to match <em>territory:</em> content
        pattern = r'<em>([^<]+):</em>\s*([^<]*?)(?=<em>|$)'
        matches = re.finditer(pattern, text, re.IGNORECASE)

        for match in matches:
            territory = clean_text(match.group(1).strip())
            content = clean_text(match.group(2).strip())

            if territory and content:
                territories[territory] = content

        return territories

    except Exception as e:
        if app_logger:
            app_logger.error(f"Error parsing territorial subdivisions: {e}")
        return {}
