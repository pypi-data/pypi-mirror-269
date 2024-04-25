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
import unittest
from everysk.config import settings

from everysk.core.datetime import DateTime, Date

from everysk.core.exceptions import RequiredError, FieldValueError

from everysk.sdk.entities.datastore.base import Datastore

###############################################################################
#   Datastore TestCase Implementation
###############################################################################
class DatastoreTestCase(unittest.TestCase):

    def setUp(self):
        self.sample_data = {
            'id': 'dats_12345678',
            'name': 'My Datastore',
            'description': 'This is a sample datastore.',
            'tags': ['tag1', 'tag2'],
            'link_uid': None,
            'workspace': 'my_workspace',
            'date': DateTime(2023, 9, 9, 9, 9, 9, 9),
            'level': '1',
            'data': {'key1': 'value1', 'key2': 'value2'},
            'version': 'v1',
            'created_on': DateTime(2023, 9, 9, 9, 9, 9, 9),
            'updated_on': DateTime(2023, 9, 9, 9, 9, 9, 9)
        }
        self.datastore = Datastore(**self.sample_data)

    def test_get_id_prefix(self):
        self.assertEqual(Datastore.get_id_prefix(), settings.DATASTORE_ID_PREFIX)

    def test_validate(self):
        datastore: Datastore = self.datastore.copy()
        with unittest.mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = True
            result = datastore.validate()

        mock_http_connection.assert_called_once_with(class_name='Datastore', params={}, method_name='validate', self_obj=datastore)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertTrue(result)

    def test_validate_error(self):
        datastore: Datastore = self.datastore.copy()
        datastore.data = DateTime.now()
        with self.assertRaisesRegex(FieldValueError, "Datastore data is not a valid json"):
            datastore.validate()

        datastore.data = None
        with self.assertRaisesRegex(RequiredError, "The data attribute is required"):
            datastore.validate()

    def test_to_dict(self):
        dict_output = self.datastore.to_dict()
        self.assertIsInstance(dict_output, dict)
        self.assertEqual(dict_output['name'], self.sample_data['name'])
        self.assertEqual(dict_output['date'], Date.strftime_or_null(self.sample_data['date']))
        self.assertEqual(dict_output['created'], self.sample_data['created_on'].timestamp())

    def test_to_dict_no_modify_obj_by_reference(self):
        datastore = Datastore(
            date=DateTime(2021, 1, 1, 1, 1, 1),
            created_on=DateTime(2021, 1, 1, 1, 1, 1),
            updated_on=DateTime(2021, 1, 1, 1, 1, 1),
            tags=['tag1', 'tag2'],
            data={'test_key': 'test_value'})
        dict_output = datastore.to_dict()

        self.assertDictEqual(
            dict_output,
            {
                'version': 'v1',
                'id': None,
                'name': None,
                'description': None,
                'tags': ['tag1',
                'tag2'],
                'link_uid': None,
                'workspace': None,
                'date': '20210101',
                'level': None,
                'data': {
                    'test_key': 'test_value'
                },
                'date_time': '20210101 01:01:01',
                'created': 1609462861,
                'updated': 1609462861
            }
        )

        dict_output['tags'].append('tag3')
        self.assertNotIn('tag3', datastore.tags)
        dict_output['data']['other_key'] = ['other_value']
        self.assertNotIn('other_key', datastore.data)

    def test_query_load_with_id(self):
        with unittest.mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = self.sample_data
            result = Datastore(id='dats_1234567891011211234567890', workspace='SampleWorkspace').load()

        mock_http_connection.assert_called_once_with(
            params={'entity_id': 'dats_1234567891011211234567890'},
            class_name='Datastore',
            method_name='retrieve',
            self_obj=None
        )
        mock_http_connection.return_value.get_response.assert_called_once_with()

        self.assertEqual(result, self.datastore)
        self.assertIsInstance(result, Datastore)

    def test_query_load(self):
        with unittest.mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = self.sample_data
            result = Datastore(link_uid='SampleLinkUID', workspace='SampleWorkspace').load()

        mock_http_connection.assert_called_once_with(
            self_obj={
                'filters': [('workspace', '=', 'SampleWorkspace'), ('link_uid', '=', 'SampleLinkUID')],
                'order': [],
                'projection': None,
                'limit': None,
                'offset': None,
                'page_size': None,
                'page_token': None,
                'distinct_on': []
            },
            params={'offset': None},
            class_name='Query',
            method_name='load'
        )
        mock_http_connection.return_value.get_response.assert_called_once_with()

        self.assertEqual(result, self.datastore)
        self.assertIsInstance(result, Datastore)
