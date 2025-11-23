######################################################################################################################
# CORE IMPORTS
# proj_004_cia\c_00_transform_utils\clean_text.py
# ---------------------------------------------------------------------------------------------------------------------
import re
import html
from proj_004_cia.__logger.logger import app_logger

######################################################################################################################
# ENHANCED CLEAN TEXT UTILITY
######################################################################################################################


def clean_text(text: str, preserve_formatting: bool = False, remove_notes: bool = False) -> str:
    """
    Enhanced text cleaning with support for complex CIA data patterns.

    Args:
        text: Raw text to clean
        preserve_formatting: If True, preserves some formatting like line breaks
        remove_notes: If True, removes content in parentheses and brackets

    Returns:
        Cleaned text string

    Examples:
        >>> clean_text("<strong>note:</strong> some text (2023 est.)")
        "note: some text (2023 est.)"

        >>> clean_text("text with <em>emphasis</em>", remove_notes=True)
        "text with emphasis"
    """
    if not isinstance(text, str) or not text:
        return ""

    try:
        original_text = text

        # Step 1: Handle HTML entities first
        html_entities = {
            '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"',
            '&apos;': "'", '&nbsp;': ' ', '&mdash;': '—', '&ndash;': '–',
            '&rsquo;': "'", '&lsquo;': "'", '&rdquo;': '"', '&ldquo;': '"',
            '&hellip;': '...', '&bull;': '•', '&middot;': '·',
            '&deg;': '°', '&plusmn;': '±', '&times;': '×', '&divide;': '÷',
            '&frac12;': '½', '&frac14;': '¼', '&frac34;': '¾',
            '&euro;': '€', '&pound;': '£', '&yen;': '¥', '&cent;': '¢',
        }
        for entity, replacement in html_entities.items():
            text = text.replace(entity, replacement)

        # Also use html.unescape for any remaining entities (numeric codes, etc.)
        text = html.unescape(text)

        # Step 2: Remove or preserve HTML tags based on context
        if preserve_formatting:
            # Convert some HTML tags to readable equivalents
            text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
            text = re.sub(r'<p[^>]*>', '\n', text, flags=re.IGNORECASE)
            text = re.sub(r'</p>', '', text, flags=re.IGNORECASE)

        # Remove all remaining HTML tags but preserve content
        text = re.sub(r'<[^>]+>', '', text)

        # Step 3: Handle notes and parenthetical content
        if remove_notes:
            # Remove content in parentheses and brackets
            text = re.sub(r'\([^)]*\)', '', text)
            text = re.sub(r'\[[^\]]*\]', '', text)

        # Step 4: Normalize whitespace
        if preserve_formatting:
            # Preserve intentional line breaks but clean up excess spaces
            # Multiple spaces/tabs to single space
            text = re.sub(r'[ \t]+', ' ', text)
            # Multiple newlines to double newline
            text = re.sub(r'\n\s*\n', '\n\n', text)
        else:
            # Standard whitespace normalization
            text = re.sub(r'\s+', ' ', text)

        # Step 5: Clean up punctuation and special characters
        text = text.replace('\u2019', "'")  # Right single quotation mark
        text = text.replace('\u2018', "'")  # Left single quotation mark
        text = text.replace('\u201c', '"')  # Left double quotation mark
        text = text.replace('\u201d', '"')  # Right double quotation mark
        text = text.replace('\u2013', '-')  # En dash
        text = text.replace('\u2014', '--')  # Em dash

        # Step 6: Final cleanup
        text = text.strip()

        # Log if significant changes were made
        if len(original_text) - len(text) > 50:
            app_logger.debug(
                f"Significant text cleaning: {len(original_text)} → {len(text)} characters")

        return text

    except Exception as e:
        app_logger.error(f"Error cleaning text: {e}")
        return text.strip() if isinstance(text, str) else ""
######################################################################################################################
