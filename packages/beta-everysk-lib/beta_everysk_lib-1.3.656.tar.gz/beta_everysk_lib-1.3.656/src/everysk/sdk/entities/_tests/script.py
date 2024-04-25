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
from unittest.mock import MagicMock

from everysk.sdk.entities.query import Query
from everysk.sdk.entities.portfolio.base import Portfolio

###############################################################################
#   Script TestCase Implementation
###############################################################################
class ScriptTestCase(TestCase):
    def setUp(self):
        self.mock_klass = MagicMock()
        self.query = Query(Portfolio)

    def test_script_query_none_user_input(self):
        result = Portfolio.script.fetch(None, 'someVariant', 'someWorkspace')
        self.assertIsNone(result)

    def test_script_query_previous_workers_without_id(self):
        user_input = {"someField": "someValue"}
        with mock.patch.object(Portfolio, '__init__', return_value=None):
            result = Portfolio.script.fetch(user_input, 'previousWorkers', 'someWorkspace')
        self.assertIsInstance(result, Portfolio)

    def test_script_query_tag_latest_variant(self):
        user_input = {"tags": "someTag"}

        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = Portfolio(name='test', workspace='someWorkspace')
            result = Portfolio.script.fetch(user_input, 'tagLatest', 'someWorkspace')
        self.assertIsInstance(result, Portfolio)
        self.assertEqual(result.name, 'test')

    def test_persist_transient(self):
        entity = Portfolio(name='test', workspace='someWorkspace')
        entity.validate = MagicMock()

        with mock.patch('everysk.sdk.entities.script.Script.get_response', return_value=entity) as mock_get_response:
            result = Portfolio.script.persist(entity, 'transient')

        mock_get_response.assert_called_once_with(self_obj=Portfolio.script, params={'entity': entity, 'persist': 'transient'})
        self.assertEqual(result, entity)
