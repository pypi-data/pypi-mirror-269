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

from everysk.sdk.entities.custom_index.base import CustomIndex

###############################################################################
#   Custom Index TestCase Implementation
###############################################################################
class CustomIndexTestCase(TestCase):

    def setUp(self):
        self.sample_data = {
            'symbol': 'CUSTOM:INDEX',
            'name': 'SampleCustomIndex',
            'tags': ['tag1', 'tag2'],
            'description': 'Description',
            'currency': 'USD',
            'data': [[1, 2, 3], [4, 5, 6]],
            'periodicity': 'M',
            'data_type': 'PRICE',
            'base_price': 100,
            'version': '1.0',
            'created_on': DateTime(2023, 9, 9, 9, 9, 9, 9),
            'updated_on': DateTime(2023, 9, 9, 9, 9, 9, 9),
        }
        self.custom_index = CustomIndex(**self.sample_data)

    def test_init(self):
        self.assertEqual(self.custom_index.symbol, self.custom_index.id)
        self.assertEqual(self.custom_index.symbol, self.sample_data['symbol'])
        self.assertEqual(self.custom_index.name, self.sample_data['name'])
        self.assertEqual(self.custom_index.tags, self.sample_data['tags'])
        self.assertEqual(self.custom_index.description, self.sample_data['description'])
        self.assertEqual(self.custom_index.currency, self.sample_data['currency'])
        self.assertEqual(self.custom_index.data, self.sample_data['data'])
        self.assertEqual(self.custom_index.periodicity, self.sample_data['periodicity'])
        self.assertEqual(self.custom_index.data_type, self.sample_data['data_type'])
        self.assertEqual(self.custom_index.base_price, self.sample_data['base_price'])
        self.assertEqual(self.custom_index.version, self.sample_data['version'])
        self.assertEqual(self.custom_index.created_on, self.sample_data['created_on'])
        self.assertEqual(self.custom_index.updated_on, self.sample_data['updated_on'])

    def test_property_id(self):
        self.assertEqual(self.custom_index.id, self.custom_index.symbol)

    def test_setter_id(self):
        self.custom_index.id = 'CUSTOM:NEW_ID'
        self.assertEqual(self.custom_index.id, 'CUSTOM:NEW_ID')
        self.assertEqual(self.custom_index.symbol, 'CUSTOM:NEW_ID')
        self.custom_index.symbol = 'CUSTOM:NEW_ID_2'
        self.assertEqual(self.custom_index.id, 'CUSTOM:NEW_ID_2')
        self.assertEqual(self.custom_index.symbol, 'CUSTOM:NEW_ID_2')

    def test_setter_id_with_invalid_value(self):
        with self.assertRaises(FieldValueError) as e:
            self.custom_index.id = 'Potato'
        self.assertEqual("The value 'Potato' for field 'symbol' must match with this regex: ^CUSTOM:[A-Z0-9_]*$.", e.exception.msg)

        with self.assertRaises(FieldValueError) as e:
            self.custom_index.symbol = 'Potato'
        self.assertEqual("The value 'Potato' for field 'symbol' must match with this regex: ^CUSTOM:[A-Z0-9_]*$.", e.exception.msg)

    def test_get_id_prefix(self):
        self.assertEqual(CustomIndex.get_id_prefix(), settings.CUSTOM_INDEX_SYMBOL_PREFIX)

    def test_validate(self):
        custom_index: CustomIndex = self.custom_index.copy()
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = True
            result = custom_index.validate()

        mock_http_connection.assert_called_once_with(class_name='CustomIndex', params={}, method_name='validate', self_obj=custom_index)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertTrue(result)

    def test_entity_to_query(self):
        custom_index: CustomIndex = self.custom_index.copy()
        query = custom_index._entity_to_query() #pylint: disable=protected-access
        self.assertListEqual(query.filters, [
            ('name', '<', 'samplecustomindey'),
            ('name', '>=', 'samplecustomindex'),
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
            CustomIndex.modify_many(entity_id_list=['CUSTOM:INDEX'], overwrites={})

    def test_clone_many(self):
        with self.assertRaises(NotImplementedError) as e:
            CustomIndex.clone_many(entity_id_list=['CUSTOM:INDEX'], overwrites={})
