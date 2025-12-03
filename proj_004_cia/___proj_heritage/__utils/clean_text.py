"""
Text cleaning and normalization utilities.

Provides functions for cleaning, normalizing, and standardizing text data.
"""

import re
from typing import Optional


def clean_text(text: Optional[str]) -> str:
    """
    Clean and normalize text content.

    Args:
        text: Raw text to clean

    Returns:
        Cleaned text with normalized whitespace

    Operations:
        - Strip leading/trailing whitespace
        - Normalize multiple spaces to single space
        - Remove control characters
        - Preserve Unicode characters (for multilingual content)

    Example:
        >>> clean_text("  Historic   Centre  ")
        'Historic Centre'

        >>> clean_text("Text\\nwith\\nlinebreaks")
        'Text with linebreaks'
    """
    if not text:
        return ""

    # Convert to string if not already
    text = str(text)

    # Remove control characters except newlines/tabs
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', text)

    # Normalize whitespace (including newlines)
    text = re.sub(r'\s+', ' ', text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


def normalize_whitespace(text: Optional[str], preserve_newlines: bool = False) -> str:
    """
    Normalize whitespace in text.

    Args:
        text: Text to normalize
        preserve_newlines: If True, keep single newlines

    Returns:
        Text with normalized whitespace

    Example:
        >>> normalize_whitespace("Line 1\\n\\n\\nLine 2")
        'Line 1 Line 2'

        >>> normalize_whitespace("Line 1\\n\\nLine 2", preserve_newlines=True)
        'Line 1\\nLine 2'
    """
    if not text:
        return ""

    text = str(text)

    if preserve_newlines:
        # Normalize multiple newlines to single
        text = re.sub(r'\n\s*\n+', '\n', text)
        # Normalize spaces/tabs on each line
        lines = [re.sub(r'[ \t]+', ' ', line.strip()) for line in text.split('\n')]
        return '\n'.join(lines)
    else:
        # Replace all whitespace with single space
        return re.sub(r'\s+', ' ', text).strip()


def truncate_text(text: str, max_length: int, suffix: str = '...') -> str:
    """
    Truncate text to maximum length, adding suffix if truncated.

    Args:
        text: Text to truncate
        max_length: Maximum length (including suffix)
        suffix: Suffix to add if truncated (default: '...')

    Returns:
        Truncated text

    Example:
        >>> truncate_text("Very long text here", 10)
        'Very lo...'
    """
    if not text or len(text) <= max_length:
        return text

    truncate_at = max_length - len(suffix)
    return text[:truncate_at] + suffix


def remove_html_tags(text: Optional[str]) -> str:
    """
    Remove HTML tags from text.

    Args:
        text: Text potentially containing HTML

    Returns:
        Text with HTML tags removed

    Example:
        >>> remove_html_tags("<p>Hello <b>World</b></p>")
        'Hello World'
    """
    if not text:
        return ""

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Clean up resulting whitespace
    return clean_text(text)


def extract_sentences(text: str, max_sentences: int = 3) -> str:
    """
    Extract first N sentences from text.

    Args:
        text: Text to extract from
        max_sentences: Maximum number of sentences

    Returns:
        First N sentences

    Example:
        >>> extract_sentences("First. Second. Third. Fourth.", 2)
        'First. Second.'
    """
    if not text:
        return ""

    # Split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Take first N sentences
    return ' '.join(sentences[:max_sentences])


if __name__ == "__main__":
    """Test text cleaning utilities with various inputs."""

    print("=" * 70)
    print("TEXT CLEANING UTILITIES TEST")
    print("=" * 70)

    # Test 1: clean_text()
    print("\n1. CLEAN TEXT FUNCTION")
    print("-" * 70)

    test_cases_clean = [
        ("  Historic   Centre  ", "Multiple spaces"),
        ("Text\nwith\nlinebreaks", "Line breaks"),
        ("\tTabbed\t\tText\t", "Tabs"),
        ("  Mixed   \n\n  whitespace  ", "Mixed whitespace"),
        ("Ünëscö Hérïtägë", "Unicode characters"),
        ("", "Empty string"),
        (None, "None value")
    ]

    for text, description in test_cases_clean:
        result = clean_text(text)
        print(f"Input  ({description}): {repr(text)}")
        print(f"Output: {repr(result)}")
        print()

    # Test 2: normalize_whitespace()
    print("\n2. NORMALIZE WHITESPACE FUNCTION")
    print("-" * 70)

    test_cases_whitespace = [
        ("Line 1\n\n\nLine 2", False, "Multiple newlines (collapsed)"),
        ("Line 1\n\nLine 2", True, "Multiple newlines (preserved)"),
        ("Word1    Word2   Word3", False, "Multiple spaces"),
        ("Para 1\n\nPara 2\n\nPara 3", True, "Paragraphs (preserved)")
    ]

    for text, preserve, description in test_cases_whitespace:
        result = normalize_whitespace(text, preserve_newlines=preserve)
        print(f"Input  ({description}): {repr(text)}")
        print(f"Preserve newlines: {preserve}")
        print(f"Output: {repr(result)}")
        print()

    # Test 3: truncate_text()
    print("\n3. TRUNCATE TEXT FUNCTION")
    print("-" * 70)

    long_text = "Inhabited since prehistoric times, Butrint has been the site of a Greek colony."

    test_cases_truncate = [
        (long_text, 30, "...", "Standard truncation"),
        (long_text, 50, " [more]", "Custom suffix"),
        ("Short text", 50, "...", "No truncation needed"),
        (long_text, 20, "…", "Unicode ellipsis")
    ]

    for text, max_len, suffix, description in test_cases_truncate:
        result = truncate_text(text, max_len, suffix)
        print(f"Test: {description}")
        print(f"Input:  {text}")
        print(f"Length: {len(text)} → {max_len} chars (suffix: {repr(suffix)})")
        print(f"Output: {result}")
        print()

    # Test 4: remove_html_tags()
    print("\n4. REMOVE HTML TAGS FUNCTION")
    print("-" * 70)

    test_cases_html = [
        ("<p>Hello <b>World</b></p>", "Basic HTML"),
        ("<div class='test'>Content <span>here</span></div>", "HTML with attributes"),
        ("Plain text without tags", "No HTML tags"),
        ("<h1>Title</h1>\n<p>Paragraph</p>", "Multiple tags with newlines")
    ]

    for html, description in test_cases_html:
        result = remove_html_tags(html)
        print(f"Input  ({description}): {repr(html)}")
        print(f"Output: {repr(result)}")
        print()

    # Test 5: extract_sentences()
    print("\n5. EXTRACT SENTENCES FUNCTION")
    print("-" * 70)

    paragraph = ("First sentence here. Second sentence follows! Third sentence too? "
                "Fourth sentence exists. Fifth one as well.")

    for num in [1, 2, 3, 5, 10]:
        result = extract_sentences(paragraph, num)
        actual_sentences = len([s for s in result.split('.') if s.strip()])
        print(f"Extract {num} sentences: Got {actual_sentences}")
        print(f"Output: {result[:80]}{'...' if len(result) > 80 else ''}")
        print()

    # Summary
    print("=" * 70)
    print("✓ All text cleaning utility tests completed!")
    print("=" * 70)
