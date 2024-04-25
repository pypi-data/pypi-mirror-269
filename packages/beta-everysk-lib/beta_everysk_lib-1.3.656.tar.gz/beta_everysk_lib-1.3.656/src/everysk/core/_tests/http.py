###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
from unittest import TestCase, mock
from everysk.core.exceptions import HttpError
from everysk.core.http import HttpConnection, HttpGETConnection, HttpPOSTConnection, requests, time


class FakeResponse:
    # https://everysk.atlassian.net/browse/COD-1047
    def __bool__(self):
        return False


class HttpConnectionTestCase(TestCase):

    def test_get_url(self):
        http = HttpConnection(url='https://test.com')
        self.assertEqual(http.url, 'https://test.com')
        self.assertEqual(http.get_url(), 'https://test.com')

    def test_clean_response_200(self):
        response = mock.MagicMock()
        response.status_code = 200
        http = HttpConnection()
        self.assertEqual(http._clean_response(response), response) # pylint: disable=protected-access

    def test_clean_response_202(self):
        response = mock.MagicMock()
        response.status_code = 200
        http = HttpConnection()
        self.assertEqual(http._clean_response(response), response) # pylint: disable=protected-access

    def test_clean_response_500(self):
        response = mock.MagicMock()
        response.status_code = 500
        http = HttpConnection()
        self.assertRaises(HttpError, http._clean_response, response) # pylint: disable=protected-access

    def test_clean_without_status_code(self):
        # https://everysk.atlassian.net/browse/COD-1047
        response = FakeResponse()
        self.assertFalse(response)
        http = HttpConnection()
        http._clean_response(response) # pylint: disable=protected-access

    def test_get_headers(self):
        http = HttpConnection()
        self.assertDictEqual(
            http.get_headers(),
            {
                'Accept-Encoding': 'gzip, deflate;q=0.9',
                'Accept-Language': 'en-US, en;q=0.9, pt-BR;q=0.8, pt;q=0.7',
                'Cache-control': 'no-cache',
                'Connection': 'close',
                'Content-Type': 'text/html; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
            }
        )

    def test_get_headers_attribute(self):
        http = HttpConnection(headers={'key': 'value'})
        self.assertDictEqual(
            http.get_headers(),
            {
                'Accept-Encoding': 'gzip, deflate;q=0.9',
                'Accept-Language': 'en-US, en;q=0.9, pt-BR;q=0.8, pt;q=0.7',
                'Cache-control': 'no-cache',
                'Connection': 'close',
                'Content-Type': 'text/html; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
                'key': 'value'
            }
        )

    def test_message_error_check(self):
        self.assertFalse(HttpConnection().message_error_check('text'))

    def test_get_response_from_url(self):
        self.assertIsNone(HttpConnection()._get_response_from_url()) # pylint: disable=protected-access

    @mock.patch.object(HttpConnection, '_clean_response', return_value='response')
    def test_get_response(self, _clean_response: mock.MagicMock):
        self.assertEqual(HttpConnection().get_response(), 'response')
        _clean_response.assert_called_once_with(None)

    @mock.patch.object(HttpConnection, '_clean_response', side_effect=HttpError('Error'))
    @mock.patch.object(HttpConnection, 'message_error_check', return_value=True)
    @mock.patch.object(time, 'sleep')
    def test_get_response_error(
        self, sleep: mock.MagicMock, message_error_check: mock.MagicMock, _clean_response: mock.MagicMock
    ):
        self.assertRaises(HttpError, HttpConnection().get_response)
        self.assertEqual(sleep.call_count, 4)
        self.assertEqual(message_error_check.call_count, 5)
        self.assertEqual(_clean_response.call_count, 5)


class HttpGETConnectionTestCase(TestCase):

    def setUp(self) -> None:
        self.old_get = requests.get
        response = mock.MagicMock()
        response.status_code = 200
        requests.get = mock.create_autospec(requests.get)
        requests.get.return_value = response

    def tearDown(self) -> None:
        requests.get = self.old_get

    def test_get_params(self):
        http = HttpGETConnection(url='https://test.com')
        self.assertIsNone(http.get_params())
        http.params = {'key': 'value'}
        self.assertDictEqual(http.get_params(), {'key': 'value'})

    def test_get_response(self):
        http = HttpGETConnection(url='https://test.com', params={'p1': 1, 'p2': 2})
        http.get_response()
        requests.get.assert_called_once_with(
            url='https://test.com',
            headers=http.get_headers(),
            params={'p1': 1, 'p2': 2},
            timeout=30
        )

    def test_user(self):
        http = HttpGETConnection(
            url='https://test.com',
            params={'p1': 1, 'p2': 2},
            user='user',
            password='pass'
        )
        http.get_response()
        requests.get.assert_called_once_with(
            url='https://test.com',
            headers=http.get_headers(),
            params={'p1': 1, 'p2': 2},
            timeout=30,
            auth=('user', 'pass')
        )


class HttpPOSTConnectionTestCase(TestCase):

    def setUp(self) -> None:
        self.old_post = requests.post
        response = mock.MagicMock()
        response.status_code = 200
        requests.post = mock.create_autospec(requests.post)
        requests.post.return_value = response

    def tearDown(self) -> None:
        requests.post = self.old_post

    def test_get_headers(self):
        http = HttpPOSTConnection(url='https://test.com')
        self.assertDictEqual(
            http.get_headers(),
            {
                'Accept-Encoding': 'gzip, deflate;q=0.9',
                'Accept-Language': 'en-US, en;q=0.9, pt-BR;q=0.8, pt;q=0.7',
                'Cache-control': 'no-cache',
                'Connection': 'close',
                'Content-Type': 'application/json; charset=utf-8',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
            }
        )

    def test_get_payload(self):
        http = HttpPOSTConnection(url='https://test.com')
        self.assertIsNone(http.get_payload())
        http.payload = {'key': 'value'}
        self.assertDictEqual(http.get_payload(), {'key': 'value'})

    def test_get_response(self):
        http = HttpPOSTConnection(url='https://test.com', payload={'p1': 1, 'p2': 2})
        http.get_response()
        requests.post.assert_called_once_with(
            headers=http.get_headers(),
            json={'p1': 1, 'p2': 2},
            url='https://test.com',
            timeout=30
        )

    def test_post_not_json(self):
        http = HttpPOSTConnection(url='https://test.com', is_json=False, payload={'p1': 1, 'p2': 2})
        http.get_response()
        self.assertDictEqual(
            http.get_headers(),
            {
                'Accept-Encoding': 'gzip, deflate;q=0.9',
                'Accept-Language': 'en-US, en;q=0.9, pt-BR;q=0.8, pt;q=0.7',
                'Cache-control': 'no-cache',
                'Connection': 'close',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
            }
        )
        requests.post.assert_called_once_with(
            headers=http.get_headers(),
            data={'p1': 1, 'p2': 2},
            url='https://test.com',
            timeout=30
        )
