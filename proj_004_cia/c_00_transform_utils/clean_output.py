"""
Utility to recursively clean all string values in nested data structures.

This ensures all output from parsers has HTML entities properly decoded
and text normalized, even if individual parsers miss calling clean_text.
"""
import html
import re
from typing import Any, Dict, List, Union


def clean_output(data: Any) -> Any:
    """
    Recursively clean all string values in a nested data structure.

    Args:
        data: Any data structure (dict, list, str, etc.)

    Returns:
        The same structure with all strings cleaned of HTML entities

    Example:
        >>> clean_output({'name': 'São Paulo &atilde;', 'items': ['test &rsquo;']})
        {'name': 'São Paulo ã', 'items': ["test '"]}
    """
    if isinstance(data, dict):
        return {k: clean_output(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_output(item) for item in data]
    elif isinstance(data, str):
        return _clean_string(data)
    else:
        return data


def _clean_string(text: str) -> str:
    """
    Clean a single string of HTML entities and normalize whitespace.
    """
    if not text:
        return text

    # Decode HTML entities
    text = html.unescape(text)

    # Normalize unicode quotes to ASCII
    text = text.replace('\u2019', "'")  # Right single quote
    text = text.replace('\u2018', "'")  # Left single quote
    text = text.replace('\u201c', '"')  # Left double quote
    text = text.replace('\u201d', '"')  # Right double quote
    text = text.replace('\u2013', '-')  # En dash
    text = text.replace('\u2014', '--') # Em dash

    # Normalize whitespace (but preserve intentional newlines)
    text = re.sub(r'[ \t]+', ' ', text)
    text = text.strip()

    return text


# Test
if __name__ == '__main__':
    test_data = {
        'name': 'São Paulo &atilde;',
        'nested': {
            'quote': "world&rsquo;s largest",
            'items': ['test &lt;1%', 'item &Iacute;']
        },
        'number': 12345,
        'none_val': None
    }

    from pprint import pprint
    print("Input:")
    pprint(test_data)
    print("\nOutput:")
    pprint(clean_output(test_data))
