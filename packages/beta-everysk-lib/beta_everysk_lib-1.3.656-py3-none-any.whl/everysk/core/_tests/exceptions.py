###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
from unittest import TestCase
from everysk.core import exceptions


class BaseExceptionTestCase(TestCase):
    cls = exceptions._BaseException # pylint: disable=protected-access

    def test_init_no_args(self):
        obj = self.cls()
        self.assertEqual(obj.msg, 'Application error.')
        self.assertEqual(str(obj), 'Application error.')

    def test_init_args(self):
        message = 'Error message.'
        obj = self.cls(message)
        self.assertEqual(obj.msg, message)
        self.assertEqual(str(obj), message)

    def test_args_later(self):
        message = 'Other test.'
        obj = self.cls('Test')
        obj.args = (message, )
        self.assertEqual(obj.args, (message,))
        self.assertEqual(obj.msg, message)
        self.assertEqual(str(obj), message)

    def test_args_error(self):
        with self.assertRaisesRegex(ValueError, "The 'args' value must be a tuple not <class 'str'>."):
            obj = self.cls('Test')
            obj.args = 'Other test'

    def test_init_kwargs(self):
        message = 'Error message.'
        obj = self.cls(msg=message)
        self.assertEqual(obj.msg, message)
        self.assertEqual(str(obj), message)


class DefaultErrorTestCase(BaseExceptionTestCase):
    cls = exceptions.DefaultError


class FieldValueErrorTestCase(BaseExceptionTestCase):
    cls = exceptions.FieldValueError

    def test_inheritance(self):
        self.assertTrue(issubclass(exceptions.FieldValueError, exceptions._BaseException)) # pylint: disable=protected-access
        self.assertTrue(issubclass(exceptions.FieldValueError, ValueError))


class HttpErrorTestCase(BaseExceptionTestCase):
    cls = exceptions.HttpError

    def test_init_no_args(self):
        obj = self.cls()
        self.assertEqual(obj.msg, 'Application error.')
        self.assertEqual(obj.status_code, 500)
        self.assertEqual(str(obj), '500 -> Application error.')

    def test_init_args(self):
        message = 'Error message.'
        obj = self.cls(message)
        self.assertEqual(obj.msg, message)
        self.assertEqual(obj.status_code, 500)
        self.assertEqual(str(obj), '500 -> Error message.')

    def test_init_kwargs(self):
        message = 'Error message.'
        obj = self.cls(msg=message, status_code=404)
        self.assertEqual(obj.msg, message)
        self.assertEqual(obj.status_code, 404)
        self.assertEqual(str(obj), '404 -> Error message.')

    def test_args_later(self):
        message = 'Other test.'
        obj = self.cls('Test')
        obj.args = (message, )
        self.assertEqual(obj.msg, message)
        self.assertEqual(str(obj), '500 -> Other test.')


class ReadonlyErrorTestCase(BaseExceptionTestCase):
    cls = exceptions.ReadonlyError


class RequiredErrorTestCase(BaseExceptionTestCase):
    cls = exceptions.RequiredError
