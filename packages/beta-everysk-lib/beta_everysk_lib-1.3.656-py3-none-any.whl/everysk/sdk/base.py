###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

###############################################################################
#   Imports
###############################################################################
from typing import Any
import inspect
import requests

from everysk.core.object import BaseDict
from everysk.core.exceptions import HttpError, SDKError
from everysk.core.http import HttpSDKPOSTConnection

###############################################################################
#   Base Entity Implementation
###############################################################################
def _parser_out(obj: Any, with_internals: bool = True) -> Any:
    """
    Recursively parse an object and its nested data structures.

    This function recursively processes the input object and its nested data structures.
    It can be used to convert objects with custom 'to_dict' and 'strftime_or_null' methods
    into dictionaries while handling common data types like dictionaries, lists, tuples, and sets.

    Args:
        obj (Any): The object to be parsed.
        with_internals (bool, optional): Flag to include internal details when parsing.
            Default is True.

    Returns:
        Any: The parsed object.

    """
    ret: Any = obj
    if hasattr(obj, 'to_dict'):
        ret = obj.to_dict(with_internals)

    elif isinstance(obj, dict):
        ret = type(obj)()
        for key, value in obj.items():
            ret[key] = _parser_out(value, with_internals)

    elif isinstance(obj, list):
        ret = type(obj)()
        for item in obj:
            ret.append(_parser_out(item, with_internals))

    elif isinstance(obj, tuple):
        ret = []
        for item in obj:
            ret.append(_parser_out(item, with_internals))
        ret = type(obj)(ret)

    elif isinstance(obj, set):
        ret = []
        for item in obj:
            ret.append(_parser_out(item, with_internals))

    elif hasattr(obj, 'strftime_or_null'):
        ret = obj.__class__.strftime_or_null(obj)

    return ret

class BaseSDK(BaseDict):
    """
    A base class for SDK classes.

    This class provides a base implementation for SDK classes.
    """
    # This is a blacklist to not create keys
    _keys_blacklist: frozenset[str] = frozenset([
        'config',
        'query',
        'script'
    ])

    @classmethod
    def get_response(cls, **kwargs: dict) -> Any:
        """
        Get a response from an SDK method.

        This method sends an HTTP POST request to a remote service and returns the response as a dictionary.

        Args:
            **kwargs (dict): Keyword arguments used to configure the HTTP request and SDK behavior.

        Keyword Args:
            class_name (str, optional): The name of the SDK class making the request.
                Defaults to the class name of the calling class.
            method_name (str, optional): The name of the SDK method making the request.
                Defaults to the name of the calling function.
            self_obj (object, optional): An instance of the calling SDK class, if applicable. Defaults to None.
            params (dict, optional): Additional parameters to include in the HTTP request. Defaults to an empty dictionary.

        Returns:
            Any: The response from the remote service.

        Raises:
            SDKError: If there is an issue with the SDK operation.
        """

        # Set default values for keyword arguments if not provided
        kwargs.setdefault('class_name', cls.__name__)
        kwargs.setdefault('method_name', inspect.stack()[1].function)
        kwargs.setdefault('self_obj', None)
        kwargs.setdefault('params', {})

        try:
            response: requests.models.Response = HttpSDKPOSTConnection(**kwargs).get_response()
        except HttpError as error:
            raise SDKError(error.msg) from error

        return response

    def to_dict(self, with_internals: bool = True) -> dict: # pylint: disable=unused-argument
        """
        Convert the object to a dictionary.

        This method converts the object to a dictionary by recursively parsing its attributes.

        Args:
            with_internals (bool, optional): Flag to include internal details when parsing.
                Default is True.

        Returns:
            dict: The object as a dictionary.

        Example usage:
            To convert an object to a dictionary:
            >>> obj = MyObject()
            >>> obj_dict = obj.to_dict()
        """
        return _parser_out(BaseDict(**self.copy()), with_internals)
