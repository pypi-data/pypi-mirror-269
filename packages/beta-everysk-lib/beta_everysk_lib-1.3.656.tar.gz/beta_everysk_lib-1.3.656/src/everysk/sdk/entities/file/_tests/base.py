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
from everysk.core.datetime import DateTime
from everysk.core.exceptions import RequiredError

from everysk.sdk.entities.file.base import File

###############################################################################
#   File TestCase Implementation
###############################################################################
class FileTestCase(TestCase):

    def setUp(self):
        self.sample_data = {
            'id': 'file_1234567891011211234567890',
            'name': 'SampleFile',
            'tags': ['tag1', 'tag2'],
            'description': 'Description',
            'link_uid': 'link_uid',
            'workspace': 'main',
            'date': DateTime(2023, 9, 9, 9, 9, 9, 9),
            'data': 'base64data',
            'url': '/1234567891011211234567890',
            'content_type': 'text/csv',
            'version': '1.0',
            'created_on': DateTime(2023, 9, 9, 9, 9, 9, 9),
            'updated_on': DateTime(2023, 9, 9, 9, 9, 9, 9),
            'hash': '4a0ed08522000734bb845f5d72673d9d113c8236',
        }
        self.file = File(**self.sample_data)

    def test_get_id_prefix(self):
        self.assertEqual(File.get_id_prefix(), settings.FILE_ID_PREFIX)

    def test_validate(self):
        file: File = self.file.copy()
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = True
            result = file.validate()

        mock_http_connection.assert_called_once_with(class_name='File', params={}, method_name='validate', self_obj=file)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertTrue(result)

    def test_entity_to_query(self):
        file: File = self.file.copy()
        query = file._entity_to_query() #pylint: disable=protected-access
        self.assertListEqual(query.filters, [
            ('workspace', '=', 'main'),
            ('link_uid', '=', 'link_uid'),
            ('name', '<', 'samplefilf'),
            ('name', '>=', 'samplefile'),
            ('date', '=', self.sample_data['date']),
            ('tags', '=', 'tag1'),
            ('tags', '=', 'tag2'),
            ('url', '=', '/1234567891011211234567890')
        ])
        self.assertEqual(query.order, [])
        self.assertEqual(query.projection, None)
        self.assertEqual(query.limit, None)
        self.assertEqual(query.offset, None)
        self.assertEqual(query.page_size, None)
        self.assertEqual(query.page_token, None)
        self.assertEqual(query.distinct_on, [])

    def test_to_dict(self):
        file: File = self.file.copy()
        file_dict = file.to_dict()
        self.assertEqual(file_dict, {
            'version': '1.0',
            'id': 'file_1234567891011211234567890',
            'name': 'SampleFile',
            'description': 'Description',
            'tags': ['tag1', 'tag2'],
            'link_uid': 'link_uid',
            'workspace': 'main',
            'date': '20230909',
            'data': 'base64data',
            'url': '/file/1234567891011211234567890',
            'content_type': 'text/csv',
            'date_time': '20230909 09:09:09',
            'hash': '4a0ed08522000734bb845f5d72673d9d113c8236',
            'created': 1694250549,
            'updated': 1694250549
        })

    def test_generate_url(self):
        file: File = self.file.copy()
        url = file.generate_url()
        with mock.patch('everysk.sdk.entities.file.base.generate_unique_id') as mock_generate_unique_id:
            mock_generate_unique_id.return_value = '1234567891011211234567890'
            url = file.generate_url()
        self.assertEqual(url, '/1234567891011211234567890')

    def test_required_fields(self):
        file: File = self.file.copy()
        file.id = None
        self.assertRaisesRegex(
            RequiredError,
            'The id attribute is required.',
            file.validate_required_fields
        )

        file.id = 'file_1234567891011211234567890'
        file.name = None
        self.assertRaisesRegex(
            RequiredError,
            'The name attribute is required.',
            file.validate_required_fields
        )

        file.name = 'SampleFile'
        file.workspace = None
        self.assertRaisesRegex(
            RequiredError,
            'The workspace attribute is required.',
            file.validate_required_fields
        )

        file.workspace = 'main'
        file.date = None
        self.assertRaisesRegex(
            RequiredError,
            'The date attribute is required.',
            file.validate_required_fields
        )

        file.date = DateTime(2023, 9, 9, 9, 9, 9, 9)
        file.hash = None
        self.assertRaisesRegex(
            RequiredError,
            'The hash attribute is required.',
            file.validate_required_fields
        )

        file.hash = '4a0ed08522000734bb845f5d72673d9d113c8236'
        file.data = None
        self.assertRaisesRegex(
            RequiredError,
            'The data attribute is required.',
            file.validate_required_fields
        )

        file.data = 'base64data'
        file.content_type = None
        self.assertRaisesRegex(
            RequiredError,
            'The content_type attribute is required.',
            file.validate_required_fields
        )

        file.content_type = 'text/csv'
        file.url = None
        self.assertRaisesRegex(
            RequiredError,
            'The url attribute is required.',
            file.validate_required_fields
        )
