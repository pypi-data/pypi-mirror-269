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

from everysk.config import settings
from everysk.core.exceptions import FieldValueError
from everysk.core.datetime import DateTime

from everysk.sdk.entities.private_security.base import PrivateSecurity

###############################################################################
#   Private Security TestCase Implementation
###############################################################################
class PrivateSecurityTestCase(TestCase):

    def setUp(self):
        self.sample_data = {
            'symbol': 'PRIVATE:SECURITY',
            'name': 'SamplePrivateSecurity',
            'tags': ['tag1', 'tag2'],
            'description': 'Description',
            'currency': 'USD',
            'data': {
                "m2m_spread": 0,
                "principal": 123.456,
                "expiry_date": "20231117",
                "starting_date": "20231108",
                "issue_date": "20231108",
                "method": "PRIVATE",
                "yield": 0,
                "events": [{
                        "date": "20231117",
                        "event_type": "V",
                        "value": 123.03
                }]},
            'instrument_type': 'PrivateFixedIncome',
            'version': '1.0',
            'created_on': DateTime(2023, 9, 9, 9, 9, 9, 9),
            'updated_on': DateTime(2023, 9, 9, 9, 9, 9, 9),
        }
        self.private_security = PrivateSecurity(**self.sample_data)

    def test_init(self):
        self.assertEqual(self.private_security.symbol, self.private_security.id)
        self.assertEqual(self.private_security.symbol, self.sample_data['symbol'])
        self.assertEqual(self.private_security.name, self.sample_data['name'])
        self.assertEqual(self.private_security.tags, self.sample_data['tags'])
        self.assertEqual(self.private_security.description, self.sample_data['description'])
        self.assertEqual(self.private_security.currency, self.sample_data['currency'])
        self.assertEqual(self.private_security.data, self.sample_data['data'])
        self.assertEqual(self.private_security.instrument_type, self.sample_data['instrument_type'])
        self.assertEqual(self.private_security.version, self.sample_data['version'])
        self.assertEqual(self.private_security.created_on, self.sample_data['created_on'])
        self.assertEqual(self.private_security.updated_on, self.sample_data['updated_on'])

    def test_property_id(self):
        self.assertEqual(self.private_security.id, self.private_security.symbol)

    def test_setter_id(self):
        self.private_security.id = 'PRIVATE:NEW_ID'
        self.assertEqual(self.private_security.id, 'PRIVATE:NEW_ID')
        self.assertEqual(self.private_security.symbol, 'PRIVATE:NEW_ID')
        self.private_security.symbol = 'PRIVATE:NEW_ID_2'
        self.assertEqual(self.private_security.id, 'PRIVATE:NEW_ID_2')
        self.assertEqual(self.private_security.symbol, 'PRIVATE:NEW_ID_2')

    def test_setter_id_with_invalid_value(self):
        with self.assertRaises(FieldValueError) as e:
            self.private_security.id = 'Potato'
        self.assertEqual("The value 'Potato' for field 'symbol' must match with this regex: ^PRIVATE:[A-Z0-9_]*$.", e.exception.msg)

        with self.assertRaises(FieldValueError) as e:
            self.private_security.symbol = 'Potato'
        self.assertEqual("The value 'Potato' for field 'symbol' must match with this regex: ^PRIVATE:[A-Z0-9_]*$.", e.exception.msg)

    def test_get_id_prefix(self):
        self.assertEqual(PrivateSecurity.get_id_prefix(), settings.PRIVATE_SECURITY_SYMBOL_PREFIX)

    def test_to_dict(self):
        private_sec = self.private_security.to_dict()
        self.assertDictEqual(private_sec, {
            'version': '1.0',
            'symbol': 'PRIVATE:SECURITY',
            'data': {'m2m_spread': 0,
            'principal': 123.456,
            'expiry_date': '20231117',
            'starting_date': '20231108',
            'issue_date': '20231108',
            'method': 'PRIVATE',
            'yield': 0,
            'events': [{
                'date': '20231117',
                'event_type': 'V',
                'value': 123.03}
            ]},
            'currency': 'USD',
            'description': 'Description',
            'name': 'SamplePrivateSecurity',
            'tags': ['tag1', 'tag2'],
            'created': 1694250549,
            'updated': 1694250549,
            'type': 'PrivateFixedIncome'
        })

    def test_validate(self):
        private_security: PrivateSecurity = self.private_security.copy()
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = True
            result = private_security.validate()

        mock_http_connection.assert_called_once_with(class_name='PrivateSecurity', params={}, method_name='validate', self_obj=private_security)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertTrue(result)

    def test_entity_to_query(self):
        private_security: PrivateSecurity = self.private_security.copy()
        query = private_security._entity_to_query() #pylint: disable=protected-access
        self.assertListEqual(query.filters, [
            ('name', '<', 'sampleprivatesecuritz'),
            ('name', '>=', 'sampleprivatesecurity'),
            ('tags', '=', 'tag1'),
            ('tags', '=', 'tag2')
        ])
        self.assertEqual(query.order, [])
        self.assertEqual(query.projection, None)
        self.assertEqual(query.limit, None)
        self.assertEqual(query.offset, None)
        self.assertEqual(query.page_size, None)
        self.assertEqual(query.page_token, None)
        self.assertEqual(query.distinct_on, [])

    def test_modify_many(self):
        with self.assertRaises(NotImplementedError) as e:
            PrivateSecurity.modify_many(entity_id_list=['PRIVATE:SECURITY'], overwrites={})

    def test_clone_many(self):
        with self.assertRaises(NotImplementedError) as e:
            PrivateSecurity.clone_many(entity_id_list=['PRIVATE:SECURITY'], overwrites={})
