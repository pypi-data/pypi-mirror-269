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
from unittest import TestCase

from everysk.config import settings
from everysk.core.datetime import Date
from everysk.core.exceptions import FieldValueError

from everysk.sdk.entities.portfolio.security import Security

###############################################################################
#   Security TestCase Implementation
###############################################################################
class TestSecurity(TestCase):

    def setUp(self):
        # Sample data for valid initialization
        self.valid_data = {
            'status': 'OK',
            'symbol': 'AAPL',
            'id': 'unique123',
            'quantity': 100.0,
            'instrument_class': 'Equity',
            'maturity_date': Date(2025, 5, 1),
            'issue_date': Date(2020, 1, 1),
            'return_date': Date(2025, 12, 31),
            'settlement': Date(2020, 1, 2),
            'display': 'Apple Inc.',
            'comparable': 'Yes',
            'previous_quantity': 50.0,
            'extra_field1': 'extra_value1',  # This should be placed in `extra_data`
            'extra_field2': 'extra_value2'   # This should also be placed in `extra_data`
        }
        self.security = Security(**self.valid_data)

    def test_initialization_with_valid_data(self):
        security = Security(**self.valid_data)
        self.assertEqual(security.status, 'OK')
        self.assertEqual(security.id, 'unique123')
        self.assertEqual(security.extra_data['extra_field1'], 'extra_value1')
        self.assertEqual(security.extra_data['extra_field2'], 'extra_value2')

    def test_from_list_conversion(self):
        headers = list(self.valid_data.keys())
        values = list(self.valid_data.values())
        security = Security.from_list(values, headers)
        self.assertEqual(security.status, 'OK')
        self.assertEqual(security.id, 'unique123')
        self.assertEqual(security.extra_data['extra_field1'], 'extra_value1')

    def test_to_dict_conversion(self):
        security = Security(**self.valid_data)
        dict_data = security.to_dict()
        self.assertEqual(dict_data['status'], 'OK')
        self.assertEqual(dict_data['id'], 'unique123')
        self.assertEqual(dict_data['symbol'], 'AAPL')
        self.assertEqual(dict_data['quantity'], 100.0)
        self.assertEqual(dict_data['instrument_class'], 'Equity')
        self.assertDictEqual(dict_data['extra_data'], {'extra_field1': 'extra_value1', 'extra_field2': 'extra_value2'})
        # Add additional checks as required.

    def test_initialization_with_extra_data(self):
        data_with_extra = self.valid_data.copy()
        data_with_extra['random_key'] = 'random_value'
        security = Security(**data_with_extra)
        self.assertEqual(security.extra_data['random_key'], 'random_value')

    def test_symbol_length_validation(self):
        invalid_data = self.valid_data.copy()
        invalid_data['symbol'] = 'A' * (settings.SYMBOL_ID_MAX_LEN + 1)
        with self.assertRaisesRegex(FieldValueError, "The length '101' for attribute 'symbol' must be between '0' and '100'."):
            Security(**invalid_data)

    def test_security_id_length_validation(self):
        invalid_data = self.valid_data.copy()
        invalid_data['id'] = '1' * (settings.SYMBOL_ID_MAX_LEN + 1)
        with self.assertRaisesRegex(FieldValueError, "The length '101' for attribute 'id' must be between '1' and '100'."):
            Security(**invalid_data)

    def test_date_conversion_on_to_dict(self):
        valid_data_with_date = self.valid_data.copy()
        valid_date = Date.fromisoformat('2022-01-01')
        valid_data_with_date['maturity_date'] = valid_date
        security = Security(**valid_data_with_date)
        dict_data = security.to_dict()
        self.assertEqual(dict_data['maturity_date'], '20220101')

    def test_extra_data_initialization(self):
        # Test that fields not in the class annotations are moved to `extra_data`
        data_with_extra = self.valid_data.copy()
        data_with_extra['extra_data'] = {'random_field': 'random_value'}
        security = Security(**data_with_extra)
        self.assertIn('random_field', security.extra_data)
        self.assertEqual(security.extra_data['random_field'], 'random_value')

    def test_extra_data_empty_after_initialization(self):
        # Test that if no extra data is present, `extra_data` is set to None
        data_without_extra = self.valid_data.copy()
        data_without_extra.pop('extra_field1')
        data_without_extra.pop('extra_field2')
        security = Security(**data_without_extra)
        self.assertIsNone(security.extra_data)

    def test_generate_security_id(self):
        security_id1 = Security.generate_security_id()
        security_id2 = Security.generate_security_id()

        self.assertIsInstance(security_id1, str)
        self.assertIsInstance(security_id2, str)
        self.assertNotEqual(security_id1, security_id2)

    def test_sort_header(self):
        headers = ['status', 'symbol', 'quantity', 'instrument_class']
        headers_cmp = ['quantity', 'instrument_class', 'status', 'symbol']
        sorted_headers = Security.sort_header(headers_cmp)
        self.assertListEqual(sorted_headers, headers)

    def test_validate_required_fields_without_id(self):
        # Test if ID gets auto-generated if not provided
        data_without_id = self.valid_data.copy()
        data_without_id.pop('id')
        security = Security(**data_without_id)
        security.validate_required_fields()
        self.assertIsNotNone(security.id)

    def test_validate_required_fields_with_id(self):
        # Test if provided ID is not changed
        data_with_id = self.valid_data.copy()
        data_with_id['id'] = 'test_id'
        security = Security(**data_with_id)
        security.validate_required_fields()
        self.assertEqual(security.id, "test_id")

    def test_date_fields_to_string(self):
        json_representation = Security(**self.valid_data).to_dict()
        self.assertEqual(json_representation['maturity_date'], '20250501')
        self.assertEqual(json_representation['issue_date'], '20200101')
        self.assertEqual(json_representation['return_date'], '20251231')
        self.assertEqual(json_representation['settlement'], '20200102')

    def test_exclude_internal_fields(self):
        json_representation = Security(**self.valid_data).to_dict(with_internals=False)
        self.assertNotIn('display', json_representation)
        self.assertNotIn('comparable', json_representation)
        self.assertNotIn('previous_quantity', json_representation)

    def test_include_internal_fields(self):
        json_representation = Security(**self.valid_data).to_dict(with_internals=True)
        self.assertIn('display', json_representation)
        self.assertEqual(json_representation['display'], self.valid_data['display'])
        self.assertIn('comparable', json_representation)
        self.assertEqual(json_representation['comparable'], self.valid_data['comparable'])
        self.assertIn('previous_quantity', json_representation)
        self.assertEqual(json_representation['previous_quantity'], self.valid_data['previous_quantity'])

    def test_get_attr(self):
        ret = Security._get_attr(self.security, 'symbol') # pylint: disable=protected-access
        self.assertEqual(ret, 'AAPL')

    def test_get_attr_in_extra_data(self):
        valid_data = self.valid_data.copy()
        valid_data['extra_data'] = {'other_key': 'other_value'}
        security = Security(**valid_data)
        ret = Security._get_attr(security, 'other_key') # pylint: disable=protected-access
        self.assertEqual(ret, 'other_value')

    def test_get_attr_fallback(self):
        ret = Security._get_attr(self.security, 'inexistent_key', Security.generate_security_id) # pylint: disable=protected-access
        self.assertIsInstance(ret, str)

    def test_get_attr_inexistent(self):
        ret = Security._get_attr(self.security, 'inexistent_key') # pylint: disable=protected-access
        self.assertIsNone(ret)

    def test_generate_consolidation_key(self):
        ret = self.security.generate_consolidation_key(['symbol', 'instrument_class'])
        self.assertEqual(ret, 'AAPL_Equity')

    def test_to_list_without_headers(self):
        ret = self.security.to_list()
        self.assertListEqual(ret, ['OK', 'unique123', 'AAPL', 100.0, 'Equity', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, '20250501', None, None, None, None, None, None, None, None, None, None, '20200101', None, None, None, None, None, None, None, None, None, None, None, '20251231', '20200102', None, {'extra_field1': 'extra_value1', 'extra_field2': 'extra_value2'}, None, 'Yes', 'Apple Inc.', None, None, 50.0])
