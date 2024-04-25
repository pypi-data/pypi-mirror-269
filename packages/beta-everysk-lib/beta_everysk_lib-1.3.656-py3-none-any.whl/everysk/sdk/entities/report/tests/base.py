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

from everysk.core.datetime import DateTime, ZoneInfo

from everysk.sdk.entities.report.base import Report

###############################################################################
#   Report TestCase Implementation
###############################################################################
class ReportTestCase(unittest.TestCase):

    def setUp(self):
        self.sample_data = {
            'created_on': None,
            'updated_on': None,
            'version': 'v1',
            'id': 'repo_12345678',
            'name': 'My Report',
            'description': 'This is a sample report.',
            'tags': ['tag1',
            'tag2'],
            'link_uid': None,
            'workspace': 'my_workspace',
            'date': DateTime(2022, 1, 1, 12, 0, tzinfo=ZoneInfo(key='UTC')),
            'widgets': [{'type': 'chart', 'data': {}}],
            'url': '/sefdsf5s54sdfsksdfs5',
            'authorization': 'private',
            'config_cascaded': {'setting1': 'value1',
            'setting2': 'value2'},
            'layout_content': {'section1': {}}
        }
        self.report = Report(**self.sample_data)

    def test_get_id_prefix(self):
        self.assertEqual(Report.get_id_prefix(), settings.REPORT_ID_PREFIX)

    def test_validate(self):
        report: Report = self.report.copy()
        with unittest.mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = True
            result = report.validate()

        mock_http_connection.assert_called_once_with(class_name='Report', params={}, method_name='validate', self_obj=report)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertTrue(result)

    def test_to_dict(self):
        dict_output = self.report.to_dict()
        self.assertDictEqual(dict_output, {
            'version': 'v1',
            'id': 'repo_12345678',
            'name': 'My Report',
            'description': 'This is a sample report.',
            'tags': ['tag1', 'tag2'],
            'link_uid': None,
            'workspace': 'my_workspace',
            'date': '20220101',
            'widgets': [{'type': 'chart', 'data': {}}],
            'url': 'https://app.everysk.com/report/sefdsf5s54sdfsksdfs5',
            'authorization': 'PRIVATE',
            'date_time': '20220101 12:00:00',
            'created': None,
            'updated': None,
            'absolute_url': 'https://app.everysk.com/report/sefdsf5s54sdfsksdfs5',
            'relative_url': '/report/sefdsf5s54sdfsksdfs5'
        })

    def test_to_dict_no_modify_obj_by_reference(self):
        report = Report(**self.sample_data)
        dict_output = report.to_dict()

        dict_output['tags'].append('tag3')
        self.assertNotIn('tag3', report.tags)
        self.assertIn('config_cascaded', report)
        self.assertNotIn('config_cascaded', dict_output)
        self.assertIn('layout_content', report)
        self.assertNotIn('layout_content', dict_output)

        self.assertEqual('/sefdsf5s54sdfsksdfs5', report.url)
        self.assertEqual('private', report.authorization)

        self.assertDictEqual(report.config_cascaded, {'setting1': 'value1', 'setting2': 'value2'})
        self.assertDictEqual(report.layout_content, {'section1': {}})

    def test_query_load_with_id(self):
        with unittest.mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = self.sample_data
            result = Report(id='repo_1234567891011211234567890', workspace='SampleWorkspace').load()

        mock_http_connection.assert_called_once_with(
            params={'entity_id': 'repo_1234567891011211234567890'},
            class_name='Report',
            method_name='retrieve',
            self_obj=None
        )
        mock_http_connection.return_value.get_response.assert_called_once_with()

        self.assertEqual(result, self.report)
        self.assertIsInstance(result, Report)

    def test_query_load(self):
        with unittest.mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = self.sample_data
            result = Report(link_uid='SampleLinkUID', workspace='SampleWorkspace').load()

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

        self.assertEqual(result, self.report)
        self.assertIsInstance(result, Report)

    def test_entity_to_query(self):
        cmp_query = Report.query.where('url', self.report.url)
        query = Report(url=self.report.url)._entity_to_query() #pylint: disable=protected-access

        self.assertDictEqual(query, cmp_query)
