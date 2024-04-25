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
from unittest import TestCase, mock

import os
import requests

from everysk.core.datetime import Date, DateTime
from everysk.core.compress import compress_json
from everysk.core.exceptions import HttpError, SDKError
from everysk.core.http import HttpSDKPOSTConnection

from everysk.sdk.base import BaseSDK

###############################################################################
#   BaseSDK TestCase Implementation
###############################################################################
class TestBaseSDK(TestCase):

    def setUp(self):
        self.default_kwargs = {
            'class_name': 'BaseSDK',
            'method_name': 'setUp',  # This will be overridden in each test method.
            'self_obj': None,
            'params': {}
        }
        self.old_post = requests.post
        self.headers = {
            'Accept-Encoding': 'gzip, deflate;q=0.9',
            'Accept-Language': 'en-US, en;q=0.9, pt-BR;q=0.8, pt;q=0.7',
            'Cache-control': 'no-cache',
            'Connection': 'close',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
            'Authorization': 'Bearer my_SID:my_TOKEN'
        }
        os.environ['EVERYSK_API_URL'] = 'https://test.com'
        os.environ['EVERYSK_API_SID'] = 'my_SID'
        os.environ['EVERYSK_API_TOKEN'] = 'my_TOKEN'
        response = mock.MagicMock()
        response.content = compress_json({'my_SID': 'teste'})
        response.status_code = 200
        requests.post = mock.create_autospec(requests.post)
        requests.post.return_value = response

    def tearDown(self) -> None:
        requests.post = self.old_post

    def test_defaults_are_set(self):
        # Using the context manager to mock HttpSDKPOSTConnection
        http = BaseSDK.get_response(**self.default_kwargs)

        requests.post.assert_called_once_with(
            url='https://test.com',
            headers=self.headers,
            timeout=30,
            data=compress_json(self.default_kwargs)
        )

    def test_automatic_class_name_assignment(self):
        # In this scenario, we are not passing 'class_name'.
        # Directly calling get_response from BaseSDK
        kwargs = {'method_name': 'test_automatic_class_name_assignment'}
        BaseSDK.get_response(**kwargs)

        expected_kwargs = {**self.default_kwargs, **kwargs, 'class_name': 'BaseSDK'}

        requests.post.assert_called_once_with(
            url='https://test.com',
            headers=self.headers,
            timeout=30,
            data=compress_json(expected_kwargs)
        )

    def test_automatic_method_name_assignment(self):
        # In this scenario, we are not passing 'class_name'.
        # Directly calling get_response from BaseSDK
        kwargs = {'class_name': 'BaseSDK'}
        BaseSDK.get_response(**kwargs)

        expected_kwargs = {**self.default_kwargs, **kwargs, 'method_name': 'test_automatic_method_name_assignment'}

        requests.post.assert_called_once_with(
            url='https://test.com',
            headers=self.headers,
            timeout=30,
            data=compress_json(expected_kwargs)
        )

    def test_get_response_raises_sdk_error_on_http_error(self):
        with mock.patch.object(HttpSDKPOSTConnection, 'get_response', side_effect=HttpError("Test HTTP Error")):
            with self.assertRaises(SDKError) as context:
                BaseSDK.get_response()
            self.assertEqual(str(context.exception), "Test HTTP Error")

    def test_to_dict_returns_dict(self):
        class TestSDK(BaseSDK):
            def to_dict(self, with_internals: bool = True) -> dict:
                return super().to_dict(with_internals)

        test_sdk = TestSDK(
            test='test',
            date=Date(2021, 1, 1),
            datetime=DateTime(2021, 1, 1, 1, 1, 1),
            date_list=[Date(2021, 1, 1)],
            datetime_list=[DateTime(2021, 1, 1, 1, 1, 1)],
            dates_dict={'date': Date(2021, 1, 1), 'datetime': DateTime(2021, 1, 1, 1, 1, 1), 'date_list': [Date(2021, 1, 1)], 'datetime_list': [DateTime(2021, 1, 1, 1, 1, 1)]},
            tuple_list=[(Date(2021, 1, 1),)],
            date_tuple=(Date(2021, 1, 1),),
            date_set=set([Date(2021, 1, 1)]),
        )
        test_sdk.obj_list = [TestSDK(
            test='test',
            date=Date(2021, 1, 1),
            datetime=DateTime(2021, 1, 1, 1, 1, 1),
        )]
        self.assertDictEqual(test_sdk.to_dict(), {
            'test': 'test',
            'date': '20210101',
            'datetime': '20210101 01:01:01',
            'date_list': ['20210101'],
            'datetime_list': ['20210101 01:01:01'],
            'dates_dict': {'date': '20210101', 'datetime': '20210101 01:01:01', 'date_list': ['20210101'], 'datetime_list': ['20210101 01:01:01']},
            'tuple_list': [('20210101',)],
            'date_tuple': ('20210101',),
            'date_set': ['20210101'],
            'obj_list': [{
                'test': 'test',
                'date': '20210101',
                'datetime': '20210101 01:01:01',
            }]
        })
