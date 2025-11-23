######################################################################################################################
# CORE IMPORTS
# proj_004_cia\c_00_transform_utils\parse_text_to_list.py
# ---------------------------------------------------------------------------------------------------------------------
from proj_004_cia.__logger.logger import app_logger
from typing import List
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# ----------------------------------------------------------------------------------------------------------------------


######################################################################################################################
# ENHANCED LIST PARSING WITH CONTEXT AWARENESS
######################################################################################################################

def parse_text_to_list(text: str,
                       respect_parentheses: bool = True,
                       smart_splitting: bool = True,
                       clean_items: bool = True) -> List[str]:
    """
    Enhanced text-to-list parsing with context-aware splitting.

    Args:
        text: Text to parse into list
        respect_parentheses: Whether to avoid splitting inside parentheses
        smart_splitting: Whether to use intelligent delimiter detection
        clean_items: Whether to clean each list item

    Returns:
        List of parsed and cleaned strings
    """
    if not isinstance(text, str) or not text.strip():
        return []

    try:
        # Clean the text first
        if clean_items:
            cleaned_text = clean_text(text)
        else:
            cleaned_text = text.strip()

        # Smart delimiter detection
        delimiters = [';', ','] if not smart_splitting else [
            ';', ',', '|', '\n']
        best_delimiter = ';'  # Default

        if smart_splitting:
            # Count occurrences of each delimiter outside parentheses
            delimiter_counts = {}
            in_parentheses = 0

            for char in cleaned_text:
                if char == '(':
                    in_parentheses += 1
                elif char == ')':
                    in_parentheses = max(0, in_parentheses - 1)
                elif char in delimiters and in_parentheses == 0:
                    delimiter_counts[char] = delimiter_counts.get(char, 0) + 1

            if delimiter_counts:
                best_delimiter = max(
                    delimiter_counts, key=delimiter_counts.get)

        # Parse with respect to parentheses if requested
        if respect_parentheses:
            segments = []
            buffer = []
            open_parentheses = 0

            for char in cleaned_text:
                if char == best_delimiter and open_parentheses == 0:
                    segments.append(''.join(buffer).strip())
                    buffer = []
                else:
                    buffer.append(char)
                    if char == '(':
                        open_parentheses += 1
                    elif char == ')':
                        open_parentheses = max(0, open_parentheses - 1)

            if buffer:
                segments.append(''.join(buffer).strip())
        else:
            # Simple split
            segments = cleaned_text.split(best_delimiter)

        # Clean and filter segments
        result = []
        for segment in segments:
            if clean_items:
                segment = clean_text(segment.strip())
            else:
                segment = segment.strip()

            if segment:
                result.append(segment)

        return result

    except Exception as e:
        if app_logger:
            app_logger.error(f"Error parsing text to list: {e}")
        return []
