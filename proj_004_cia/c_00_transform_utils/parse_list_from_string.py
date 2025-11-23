######################################################################################################################
# CORE IMPORTS
# C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\c_00_transform_utils\parse_list_from_string.py
# ---------------------------------------------------------------------------------------------------------------------
import re
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.__logger.logger import app_logger
from typing import Dict, Any, List, Optional, Union, Tuple
# ---------------------------------------------------------------------------------------------------------------------

######################################################################################################################
# ENHANCED LIST PARSING
######################################################################################################################


def parse_list_from_string(data_string: str,
                           delimiter: str = ',',
                           strip_items: bool = True,
                           remove_empty: bool = True,
                           clean_items: bool = True,
                           smart_delimiters: bool = True) -> List[str]:
    """
    Enhanced list parsing with smart delimiter detection and cleaning.

    Args:
        data_string: String to split into list
        delimiter: Primary delimiter to use
        strip_items: Whether to strip whitespace from items
        remove_empty: Whether to remove empty items
        clean_items: Whether to clean each item using clean_text
        smart_delimiters: Whether to auto-detect best delimiter

    Returns:
        List of cleaned strings
    """
    if not isinstance(data_string, str) or not data_string.strip():
        return []

    try:
        text = data_string.strip()

        # Smart delimiter detection
        if smart_delimiters:
            delimiter_candidates = [';', ',', '|', '\n', '•', '–', '-']
            delimiter_counts = {d: text.count(d) for d in delimiter_candidates}

            # Find the most frequent delimiter (but at least 1 occurrence)
            best_delimiter = max(delimiter_counts, key=delimiter_counts.get)
            if delimiter_counts[best_delimiter] > 0:
                delimiter = best_delimiter

        # Special handling for bullet points and numbered lists
        if '•' in text or re.search(r'\d+\.\s+', text):
            # Handle bullet points
            text = re.sub(r'[•\-–]\s*', delimiter + ' ', text)
            # Handle numbered lists
            text = re.sub(r'\d+\.\s+', delimiter + ' ', text)

        # Split the string
        items = text.split(delimiter)

        # Process each item
        processed_items = []
        for item in items:
            if strip_items:
                item = item.strip()

            if clean_items:
                item = clean_text(item)

            # Remove common prefixes/suffixes
            item = re.sub(r'^(and\s+|or\s+)', '', item, flags=re.IGNORECASE)
            item = re.sub(r'\s+(etc\.?|among others)$',
                          '', item, flags=re.IGNORECASE)

            if remove_empty and not item:
                continue

            processed_items.append(item)

        if app_logger and len(processed_items) > 0:
            app_logger.debug(
                f"Parsed {len(processed_items)} items using delimiter '{delimiter}'")

        return processed_items

    except Exception as e:
        if app_logger:
            app_logger.error(
                f"Error parsing list from string '{data_string}': {e}")
        return []
