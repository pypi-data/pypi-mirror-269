###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
__all__ = ['compress_json', 'decompress_json', 'compress_pickle', 'decompress_pickle']
import json
import pickle
import zlib
from typing import Any
from everysk.core.datetime import DateTime, Date


## Private functions
def _default(obj: Any) -> str: # pylint: disable=inconsistent-return-statements
    """
    Is used on JSONEncoder to convert objects to JSON format.

    Args:
        obj (Any): The object that needs to be changed into JSON format.
    """
    if Date.is_date(obj) or DateTime.is_datetime(obj):
        return obj.isoformat()

    if obj == Undefined:
        return Undefined.default_parse_string


def _json_parser(obj: Any) -> Any:
    """
    Transforms all strings in their correct objects.

    Args:
        obj (Any): The object that needs to be changed into object.
    """
    ret = obj
    if isinstance(obj, dict):
        ret = {}
        for key, value in obj.items():
            ret[key] = _json_parser(value)

    elif isinstance(obj, list):
        ret = []
        for item in obj:
            ret.append(_json_parser(item))

    elif isinstance(obj, str):
        # Can be date/datetime string, the Undefined string or a real string
        try:
            ret = Date.fromisoformat(obj)
        except ValueError:
            try:
                ret = DateTime.fromisoformat(obj)
            except ValueError:
                pass

        if obj == Undefined.default_parse_string:
            ret = Undefined

    return ret


## Public functions
def compress_json(obj: Any) -> str:
    """
    Convert obj to string with json dumps then uses zlib to compress it.
    To convert str json dumps return to bytes, we use encode('utf-8') method on the string.
    https://bobbyhadz.com/blog/python-json-bytes-like-object-is-required-not-str
    """
    return zlib.compress(json.dumps(obj, default=_default).encode('utf-8'))


def decompress_json(data: str) -> Any:
    """
    Decompress data with zlib and transform to a obj with json loads.
    """
    return _json_parser(json.loads(zlib.decompress(data)))


def compress_pickle(obj: Any) -> str:
    """
    Convert obj to string with pickle dumps then uses zlib to compress it.
    """
    return zlib.compress(pickle.dumps(obj))


def decompress_pickle(data: str) -> Any:
    """
    Decompress data with zlib and transform to a obj with pickle loads.
    """
    return pickle.loads(zlib.decompress(data))
