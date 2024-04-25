###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
from typing import Any
from re import compile as compile_re
from importlib import import_module
from unicodedata import normalize
from six import string_types, ensure_str, text_type


RE_ISIN = compile_re(r'^[a-zA-Z]{2}\s*[0-9a-zA-Z]{9}[0-9](?![0-9a-zA-Z-])$')


def import_from_string(dotted_path: str) -> type:
    """
    Import and return a Python class or module based on a dotted path.

    Args:
        dotted_path (str): The dotted path to the Python class or module.

    Returns:
        type: The imported Python class or module.

    Raises:
        ImportError: If the provided dotted path is invalid or if the class/module cannot be imported.

    Example usage:
        Import a class or module based on a dotted path:
        >>> import_from_string("module_name.ClassName")
        <class 'module_name.ClassName'>

    Example of exception message:
        'ImportError: "invalid.path" doesn't look like a module path.'
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as error:
        raise ImportError(f"{dotted_path} doesn't look like a module path.") from error

    module = import_module(module_path)
    try:
        return getattr(module, class_name)
    except AttributeError as error:
        raise ImportError(f'Module "{module_path}" does not define a "{class_name}" class.') from error


def is_string_object(obj: Any) -> bool:
    """
    Check if the provided object is a string object.

    Args:
        obj (Any): The object to check.

    Returns:
        bool: True if the object is a string, False otherwise.
    """
    return isinstance(obj, string_types)


def to_string(value: str) -> str:
    """
    Convert a value to a string representation.

    Args:
        value (str): The value to convert to a string.

    Returns:
        str: The string representation of the value.

    Example usage:
        Convert a value to a string:
        >>> to_string(42)
        '42'
    """
    if is_string_object(value):
        return ensure_str(value)
    return text_type(value)


def normalize_string(value: str):
    """
    Normalize a string by applying Unicode normalization (NFKD).

    Args:
        value (str): The string to normalize.

    Returns:
        str: The normalized string.
    """
    value = normalize('NFKD', value)
    return value


def normalize_string_to_search(value):
    """
    Normalize a string for search purposes by lowercasing and applying Unicode normalization (NFKD).

    Args:
        value: The string to normalize.

    Returns:
        str: The normalized and lowercase string suitable for searching.
    """
    value = value.lower().strip()
    value = to_string(value)
    return normalize_string(value)


def is_isin_string_regex(isin: str) -> bool:
    """
    Check if a provided string matches the ISIN (International Securities Identification Number) format using regex.

    Args:
        isin (str): The string to check.

    Returns:
        bool: True if the string matches the ISIN format, False otherwise.
    """
    if not isinstance(isin, string_types):
        return False
    return True if RE_ISIN.match(isin) else False
