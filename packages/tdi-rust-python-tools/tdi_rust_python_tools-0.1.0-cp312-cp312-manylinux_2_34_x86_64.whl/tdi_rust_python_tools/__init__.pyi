def remove_null_values(value: str) -> str: ...

"""Replaces values with `None` if value is in constant of "null values".

Examples: "N/A", "Null", "-" etc.

Args:
    value (str): Value to be cleaned of Null Values

Returns:
    str: Original value, or empty string if a null value was provided
"""

def combine_dedupe_values(values: list[str], separator: str) -> str: ...

"""Take a list of values, split them by a separator, and combine them into a single string with no duplicates."""

def fix_lt_gt(value: str) -> str: ...

"""Adds a space character after each "<" or ">" symbol in a string, as long as the symbol is not an HTML tag.

Returns the modified string.

Args:
    value (str): The input string to be modified.

Returns:
    str: The modified string, with a space character added after each "<" or ">" symbol that is not part of an HTML
    tag.

Examples:
    >>> fix_lt_gt("<p><90%</p>")
    "<p>< 90%</p>"

    >>> fix_lt_gt("<p>This is<em>>90% pure</em>.</p>")
    "<p>This is<em>> 90% pure</em>.</p>"
"""

def unescape_html_chars(value: str) -> str: ...

"""Unescapes HTML characters from `value` (e.g. "100 &mu;g" returns "100 µg")."""

def clean_temperature(value: str) -> str: ...

"""Cleans common issues with 'Degrees Celsius' values.

Changes any non ° characters to a °
Fixes the combined degree C character

"""

def remove_chinese_chars(value: str) -> str: ...

"""Removes all Chinese characters from `value`."""
