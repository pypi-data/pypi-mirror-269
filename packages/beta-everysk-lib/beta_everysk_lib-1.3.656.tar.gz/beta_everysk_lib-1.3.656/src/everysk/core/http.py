###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
#
# Classes that handle HTTP Connections.

# Url: https://requests.readthedocs.io/en/latest/
#      https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers
#      https://developer.mozilla.org/en-US/docs/Glossary/Quality_values
#
import random
import time
from os import getenv

import requests
from everysk.core.exceptions import HttpError
from everysk.core.fields import BoolField, DictField, IntField, ReadonlyListField, StrField
from everysk.core.object import BaseObject
from everysk.core.compress import compress_json, decompress_json


class HttpConnection(BaseObject):
    """
    Base class to use for HTTP connections, has two attributes:
        - timeout: It's in and represent seconds, defaults to 30.
        - url: It's string and will be the destination.
    """
    ## Private attributes
    _count = 1

    # 200 - Default for success
    # 202 - Default for success, but response is being processed.
    _success_status_codes = ReadonlyListField(default=[200, 202])

    ## Public attributes
    headers = DictField(default=None)
    timeout = IntField(default=30)
    url = StrField(default=None)

    def _clean_response(self, response: requests.models.Response) -> requests.models.Response:
        """
        Checks status_code for response, if status_code is different than 200 throws an exception.

        Args:
            response (requests.models.Response): Http response from server.

        Raises:
            HttpError: If something goes wrong raise exception with status_code and content.
        """
        if getattr(response, 'status_code', self._success_status_codes[0]) not in self._success_status_codes:
            raise HttpError(status_code=response.status_code, msg=response.content)

        return response

    def get_headers(self) -> dict:
        """
        Headers needed to send HTTP methods.
        Below are the most common Headers used by browsers,
        we use them to look less like a Bot and more like a valid access.
        """
        headers = {
            'Accept-Encoding': 'gzip, deflate;q=0.9',
            'Accept-Language': 'en-US, en;q=0.9, pt-BR;q=0.8, pt;q=0.7',
            'Cache-control': 'no-cache',
            'Connection': 'close', # Remove on HTTP/2 requests
            'Content-Type': 'text/html; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }
        if self.headers is not None:
            headers.update(self.headers)

        return headers

    def get_url(self) -> str:
        """
        Generate the correct url to fetch data from vendor on POST/GET requests.
        """
        return self.url

    def message_error_check(self, message: str) -> bool: # pylint: disable=unused-argument
        """
        If this method returns True, the connection will be tried again.

        Args:
            message (str): The error message that occurred on the connection.
        """
        return False

    def _get_response_from_url(self) -> requests.models.Response:
        """
        This will be implemented on child classes to really do the connection.
        """
        return None

    def get_response(self) -> requests.models.Response:
        """
        Try to fetch data from self.get_url and calling self._get_response_from_url for the complete response.
        On HttpError, if self.message_error_check is True we will try connect again more 5 times.
        """
        try:
            response = self._clean_response(self._get_response_from_url())
        except Exception as error: # pylint: disable=broad-exception-caught
            # Sometimes it can happen that the server is busy, if this happen the error message must be tested
            # and must return true to enable recursion and we will try again the connection.
            if self.message_error_check(str(error).lower()) and self._count < 5:
                self._count += 1
                # As we have several processes, we use a random number to avoid collision between them.
                time.sleep(random.randint(10, 120))
                response = self.get_response()
            else:
                raise error

        return response


class HttpGETConnection(HttpConnection):
    """ Class that implements a interface for HTTP GET connections """
    params = DictField()
    user = StrField()
    password = StrField()

    def get_params(self) -> dict:
        """
        This method is used to make the correct params to pass on GET request.
        These params will be added to the URL with & separating then.
        """
        return self.params

    def _get_response_from_url(self) -> requests.models.Response:
        """
        Try to fetch data from url using GET request.
        Note that any dictionary key whose value is None will not be added to the URL's query string.
        """
        params = {
            'url': self.get_url(),
            'headers': self.get_headers(),
            'params': self.get_params(),
            'timeout': self.timeout
        }
        if self.user:
            params['auth'] = (self.user, self.password)

        return requests.get(**params)


class HttpPOSTConnection(HttpConnection):
    """
    Class that implements a interface for HTTP POST connections.
    If self.is_json is True the POST method will be a JSON POST,
    otherwise will be a Form POST Data.
    """
    is_json = BoolField(default=True)
    payload = DictField()

    def get_headers(self) -> dict:
        """ Headers needed to send HTTP Post methods. """
        headers = super().get_headers()
        if self.is_json:
            headers['Content-Type'] = 'application/json; charset=utf-8'
        else:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'

        return headers

    def get_payload(self) -> dict:
        """ Make the correct payload body to pass on POST request. """
        return self.payload

    def _get_response_from_url(self) -> requests.models.Response:
        """ Try to get/set data on url using POST request. """
        params = {
            'url': self.get_url(),
            'headers': self.get_headers(),
            'timeout': self.timeout
        }
        if self.is_json:
            params['json'] = self.get_payload()
        else:
            params['data'] = self.get_payload()

        response = requests.post(**params)
        return response

class HttpPOSTCompressedConnection(HttpPOSTConnection):

    def get_payload(self) -> dict:
        """ Make the correct payload body to pass on POST request. """
        return compress_json(self.payload)

    def get_response(self) -> dict:
        """
        Try to fetch data from self.get_url and calling self._get_response_from_url for the complete response.
        On HttpError, if self.message_error_check is True we will try connect again more 5 times.
        Decompress the response.content
        """
        response = super().get_response()
        return decompress_json(response.content)

class HttpSDKPOSTConnection(HttpPOSTCompressedConnection):

    is_json = BoolField(default=False, readonly=True)

    class_name = StrField()
    method_name = StrField()
    self_obj = DictField()
    params = DictField()

    def __init__(self, **kwargs) -> None:
        if 'url' not in kwargs or kwargs['url'] is None:
            kwargs['url'] = getenv('EVERYSK_API_URL', None)
        super().__init__(**kwargs)

    def get_payload(self) -> dict:
        """ Make the correct payload body to pass on POST request. """
        self.payload = {
            'class_name': self.class_name,
            'method_name': self.method_name,
            'self_obj': self.self_obj,
            'params': self.params
        }
        return super().get_payload()

    def get_headers(self) -> dict:
        """ Headers needed to send HTTP Post methods. """
        headers = super().get_headers()
        everysk_api_sid = getenv('EVERYSK_API_SID', None)
        everysk_api_token = getenv('EVERYSK_API_TOKEN', None)

        headers['Authorization'] = f'Bearer {everysk_api_sid}:{everysk_api_token}'

        return headers
