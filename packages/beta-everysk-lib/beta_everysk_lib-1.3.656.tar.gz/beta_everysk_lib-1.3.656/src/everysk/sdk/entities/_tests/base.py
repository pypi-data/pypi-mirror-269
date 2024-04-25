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

from everysk.core.exceptions import RequiredError
from everysk.core.datetime.datetime import DateTime, timezone, ZoneInfo

from everysk.sdk.entities.base import BaseEntity
from everysk.sdk.entities.portfolio.base import Portfolio
from everysk.sdk.entities.portfolio.securities import Securities

###############################################################################
#   Base Entity TestCase Implementation
###############################################################################
class TestBaseEntity(TestCase):

    def setUp(self):
        self.expected_response = {
            'filters': [],
            'order': [],
            'projection': None,
            'limit': None,
            'offset': None,
            'page_size': None,
            'page_token': None,
            'distinct_on': []
        }
        self.sample_portfolio_data = {
            'id': 'port_1234567891011211234567890',
            'workspace': 'SampleWorkspace',
            'name': 'SamplePortfolio',
            'tags': ['tag1', 'tag2'],
            'link_uid': 'ABC',
            'description': 'Description',
            'nlv': 1000.0,
            'base_currency': 'USD',
            'date': DateTime.fromisoformat('20231122'),
            'securities': Securities([{'symbol': 'AAPL'}]),
            'version': '1.0',
            'created_on': DateTime.now(),
            'updated_on': DateTime.now(),
            'level': 'HIGH',
            'outstanding_shares': 1000,
            'source_hash': 'XYZ',
            'status': 'OK',
            'portfolio_uid': 'UID123',
            'check_securities': False
        }
        self.portfolio = Portfolio(**self.sample_portfolio_data)

    def test_entity_to_query(self):
        _query = self.portfolio._entity_to_query() # pylint: disable=protected-access
        self.assertDictEqual(_query,
        {
            'filters': [('workspace', '=', 'SampleWorkspace'),
            ('link_uid', '=',
            'ABC'),
                ('name', '<', 'sampleportfolip'),
                ('name', '>=', 'sampleportfolio'),
                ('date', '=', DateTime(2023, 11, 22, 0, 0, tzinfo=ZoneInfo(key='UTC'))),
                ('tags', '=', 'tag1'),
                ('tags', '=', 'tag2')],
            'order': [],
            'projection': None,
            'limit': None,
            'offset': None,
            'page_size': None,
            'page_token': None,
            'distinct_on': []
        })

    def test_get_id_prefix(self):
        with self.assertRaises(NotImplementedError):
            BaseEntity.get_id_prefix()

    def test_generate_id(self):
        with mock.patch.object(BaseEntity, 'get_id_prefix', return_value='P'), \
                mock.patch('everysk.sdk.entities.base.generate_random_id', return_value='12345'):
            self.assertEqual(BaseEntity.generate_id(), 'P12345')

    def test_validate_id(self):
        with mock.patch.object(BaseEntity, '__init__', side_effect=Exception("Mocked Exception")):
            self.assertFalse(BaseEntity.validate_id('invalid_id'))

        with mock.patch.object(BaseEntity, '__init__', return_value=None):
            self.assertTrue(BaseEntity.validate_id('valid_id'))

        with mock.patch.object(BaseEntity, '__init__', return_value=None):
            self.assertFalse(BaseEntity.validate_id(''))

        with mock.patch.object(BaseEntity, '__init__', return_value=None):
            self.assertFalse(BaseEntity.validate_id(None))

    def test_validate(self):
        self.assertTrue(BaseEntity(id="my_id", workspace="my_workspace", name="my_name", created_on=DateTime.now(), updated_on=DateTime.now()).validate())

    def test_raises_validate(self):
        base_entity = BaseEntity()
        self.assertRaisesRegex(
            RequiredError,
            'The created_on attribute is required.',
            base_entity.validate
        )

    def test_get_query(self):
        """ Test _get_query method """
        expected_response = self.expected_response.copy()
        expected_response['projection'] = ['securities']
        result = Portfolio.query.set_projection('securities') # pylint: disable=protected-access
        self.assertDictEqual(result, expected_response)

    def test_query(self):
        """ Test query method """
        expected_response = self.expected_response.copy()
        expected_response['projection'] = ['securities']
        result = Portfolio.query.set_projection('securities')
        self.assertDictEqual(result, expected_response)

    def test_where(self):
        """ Test where method """
        expected_response = self.expected_response.copy()
        expected_response['filters'] = [('date', '=', DateTime(2023, 8, 10, 12, 0, tzinfo=timezone.utc))]
        result = Portfolio.query.where('date', '=', '2023-08-10')
        self.assertDictEqual(result, expected_response)

    def test_sort_by(self):
        """ Test sort_by method """
        expected_response = self.expected_response.copy()
        expected_response['order'] = ['date']
        result = Portfolio.query.sort_by('date')
        self.assertDictEqual(result, expected_response)

    def test_set_projection(self):
        """ Test set_projection method """
        expected_response = self.expected_response.copy()
        expected_response['projection'] = ['securities']
        result = Portfolio.query.set_projection('securities')
        self.assertDictEqual(result, expected_response)

    def test_set_limit(self):
        """ Test set_limit method """
        expected_response = self.expected_response.copy()
        expected_response['limit'] = 5
        result = Portfolio.query.set_limit(5)
        self.assertDictEqual(result, expected_response)

    def test_set_offset(self):
        """ Test set_offset method """
        expected_response = self.expected_response.copy()
        expected_response['offset'] = 10
        result = Portfolio.query.set_offset(10)
        self.assertDictEqual(result, expected_response)

    def test_set_page_size(self):
        """ Test set_page_size method """
        expected_response = self.expected_response.copy()
        expected_response['page_size'] = 15
        result = Portfolio.query.set_page_size(15)
        self.assertDictEqual(result, expected_response)

    def test_set_page_token(self):
        """ Test set_page_token method """
        expected_response = self.expected_response.copy()
        expected_response['page_token'] = 'my_test_page'
        result = Portfolio.query.set_page_token('my_test_page')
        self.assertDictEqual(result, expected_response)

    def test_load(self):
        """ Test find method """
        expected_response = self.expected_response.copy()
        expected_response['filters'] = [('workspace', '=', 'my_workspace')]

        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            result = Portfolio.query.where('workspace', 'my_workspace').load(offset=5)

        mock_http_connection.assert_any_call(class_name='Query', params={'offset': 5}, method_name='load', self_obj=expected_response)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertIsInstance(result, Portfolio)

    def test_list(self):
        """ Test list method """
        expected_response = self.expected_response.copy()
        expected_response['filters'] = [('workspace', '=', 'my_workspace')]

        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            Portfolio.query.where('workspace', 'my_workspace').loads(limit=10, offset=5)

        mock_http_connection.assert_any_call(class_name='Query', params={'limit': 10, 'offset': 5}, method_name='loads', self_obj=expected_response)
        mock_http_connection.return_value.get_response.assert_called_once_with()

    def test_page(self):
        """ Test page method """
        expected_response = self.expected_response.copy()
        expected_response['filters'] = [('workspace', '=', 'my_workspace')]

        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            Portfolio.query.where('workspace', 'my_workspace').page(page_size=10, page_token='page_token')

        mock_http_connection.assert_any_call(class_name='Query', params={'page_size': 10, 'page_token': 'page_token'}, method_name='page', self_obj=expected_response)
        mock_http_connection.return_value.get_response.assert_called_once_with()

    def test_pages(self):
        """ Test pages method """
        expected_response = self.expected_response.copy()
        expected_response['filters'] = [('workspace', '=', 'my_workspace')]

        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            result = Portfolio.query.where('workspace', 'my_workspace').pages(page_size=10)
            next(result)

        mock_http_connection.assert_any_call(class_name='Query', params={'page_size': 10, 'page_token': Undefined}, method_name='page', self_obj=expected_response)
        mock_http_connection.return_value.get_response.assert_called_once_with()

    def test_script_query(self):
        """ Test script_query method """
        expected_response = self.expected_response.copy()
        expected_response['filters'] = [('workspace', '=', 'my_workspace')]

        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            Portfolio.script.fetch(user_input='port_12456', variant='select', workspace=None)

        mock_http_connection.assert_any_call(self_obj={}, params={'user_input': 'port_12456', 'variant': 'select', 'workspace': None}, class_name='Script', method_name='fetch')
        mock_http_connection.return_value.get_response.assert_called_once_with()

    def test_retrieve(self):
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = self.sample_portfolio_data
            result = Portfolio.retrieve(entity_id=self.sample_portfolio_data['id'])

        mock_http_connection.assert_any_call(class_name='Portfolio', params={'entity_id': self.sample_portfolio_data['id']}, method_name='retrieve', self_obj=None)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertEqual(result, self.portfolio)
        self.assertIsInstance(result, Portfolio)

    def test_retrieve_with_none(self):
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = None
            result = Portfolio.retrieve(entity_id=self.sample_portfolio_data['id'])

        mock_http_connection.assert_any_call(class_name='Portfolio', params={'entity_id': self.sample_portfolio_data['id']}, method_name='retrieve', self_obj=None)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertIsNone(result)

    def test_create(self):
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = self.sample_portfolio_data
            result = Portfolio.create(entity_dict=self.sample_portfolio_data)

        mock_http_connection.assert_any_call(class_name='Portfolio', params={'entity_dict': self.sample_portfolio_data}, method_name='create', self_obj=None)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertEqual(result, self.portfolio)
        self.assertIsInstance(result, Portfolio)

    def test_modify(self):
        sample_portfolio_data = self.sample_portfolio_data.copy()
        sample_portfolio_data['base_currency'] = 'BRL'
        modified_portfolio = Portfolio(**sample_portfolio_data)
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = sample_portfolio_data
            result = Portfolio.modify(entity_id=self.sample_portfolio_data['id'], overwrites={'base_currency': 'BRL'})

        mock_http_connection.assert_any_call(class_name='Portfolio', params={'entity_id': self.sample_portfolio_data['id'], 'overwrites': {'base_currency': 'BRL'}}, method_name='modify', self_obj=None)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertEqual(result, modified_portfolio)
        self.assertIsInstance(result, Portfolio)

    def test_modify_return_none(self):
        sample_portfolio_data = self.sample_portfolio_data.copy()
        sample_portfolio_data['base_currency'] = 'BRL'
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = None
            result = Portfolio.modify(entity_id=self.sample_portfolio_data['id'], overwrites={'base_currency': 'BRL'})

        mock_http_connection.assert_any_call(class_name='Portfolio', params={'entity_id': self.sample_portfolio_data['id'], 'overwrites': {'base_currency': 'BRL'}}, method_name='modify', self_obj=None)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertIsNone(result)

    def test_remove(self):
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = self.sample_portfolio_data
            result = Portfolio.remove(entity_id=self.sample_portfolio_data['id'])

        mock_http_connection.assert_any_call(class_name='Portfolio', params={'entity_id': self.sample_portfolio_data['id']}, method_name='remove', self_obj=None)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertEqual(result, self.portfolio)
        self.assertIsInstance(result, Portfolio)

    def test_remove_return_none(self):
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = None
            result = Portfolio.remove(entity_id=self.sample_portfolio_data['id'])

        mock_http_connection.assert_any_call(class_name='Portfolio', params={'entity_id': self.sample_portfolio_data['id']}, method_name='remove', self_obj=None)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertIsNone(result)

    def test_clone(self):
        sample_portfolio_data = self.sample_portfolio_data.copy()
        sample_portfolio_data['base_currency'] = 'BRL'
        modified_portfolio = Portfolio(**sample_portfolio_data)
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = sample_portfolio_data
            result = Portfolio.clone(entity_id=self.sample_portfolio_data['id'], overwrites={'base_currency': 'BRL'})

        mock_http_connection.assert_any_call(class_name='Portfolio', params={'entity_id': self.sample_portfolio_data['id'], 'overwrites': {'base_currency': 'BRL'}}, method_name='clone', self_obj=None)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertEqual(result, modified_portfolio)
        self.assertIsInstance(result, Portfolio)

    def test_clone_return_none(self):
        sample_portfolio_data = self.sample_portfolio_data.copy()
        sample_portfolio_data['base_currency'] = 'BRL'
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = None
            result = Portfolio.clone(entity_id=self.sample_portfolio_data['id'], overwrites={'base_currency': 'BRL'})

        mock_http_connection.assert_any_call(class_name='Portfolio', params={'entity_id': self.sample_portfolio_data['id'], 'overwrites': {'base_currency': 'BRL'}}, method_name='clone', self_obj=None)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertIsNone(result)

    def test_create_many(self):
        sample_portfolio_data = self.sample_portfolio_data.copy()
        sample_portfolio_data['base_currency'] = 'BRL'
        sample_portfolio_data['check_securities'] = True

        res_modified_portfolio = sample_portfolio_data.copy()
        res_modified_portfolio['check_securities'] = False

        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = [self.sample_portfolio_data, res_modified_portfolio]
            result = Portfolio.create_many(entity_dict_list=[self.sample_portfolio_data, sample_portfolio_data])

        mock_http_connection.assert_any_call(class_name='Portfolio', params={'entity_dict_list': [self.sample_portfolio_data, sample_portfolio_data]}, method_name='create_many', self_obj=None)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertIsInstance(result, list)
        self.assertEqual(result[0], self.portfolio)
        self.assertEqual(result[1], res_modified_portfolio)
        self.assertIsInstance(result[0], Portfolio)
        self.assertIsInstance(result[1], Portfolio)

    def test_modify_many(self):
        original_portfolio_data = self.sample_portfolio_data.copy()
        original_portfolio_data['name'] = 'modified_1'
        original_portfolio = Portfolio(**original_portfolio_data)

        sample_portfolio_data = self.sample_portfolio_data.copy()
        sample_portfolio_data['id'] = 'port_1234567891011211234567891'
        sample_portfolio_data['name'] = 'modified_2'
        modified_portfolio = Portfolio(**sample_portfolio_data)

        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = [original_portfolio_data, sample_portfolio_data]
            result = Portfolio.modify_many(entity_id_list=[self.sample_portfolio_data['id'], sample_portfolio_data['id']], overwrites=[{'name': 'modified_1'}, {'name': 'modified_2'}])

        mock_http_connection.assert_any_call(class_name='Portfolio', params={'entity_id_list': [self.sample_portfolio_data['id'], modified_portfolio['id']], 'overwrites': [{'name': 'modified_1'}, {'name': 'modified_2'}]}, method_name='modify_many', self_obj=None)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertIsInstance(result, list)
        self.assertEqual(result[0], original_portfolio)
        self.assertEqual(result[1], modified_portfolio)
        self.assertIsInstance(result[0], Portfolio)
        self.assertIsInstance(result[1], Portfolio)

    def test_remove_many(self):
        sample_portfolio_data = self.sample_portfolio_data.copy()
        sample_portfolio_data['id'] = 'port_1234567891011211234567891'
        sample_portfolio_data['base_currency'] = 'BRL'
        modified_portfolio = Portfolio(**sample_portfolio_data)

        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = [self.sample_portfolio_data, sample_portfolio_data]
            result = Portfolio.remove_many(entity_id_list=[self.sample_portfolio_data['id'], sample_portfolio_data['id']])

        mock_http_connection.assert_any_call(class_name='Portfolio', params={'entity_id_list': [self.sample_portfolio_data['id'], sample_portfolio_data['id']]}, method_name='remove_many', self_obj=None)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertIsInstance(result, list)
        self.assertEqual(result[0], self.portfolio)
        self.assertEqual(result[1], modified_portfolio)
        self.assertIsInstance(result[0], Portfolio)
        self.assertIsInstance(result[1], Portfolio)

    def test_clone_many(self):
        original_portfolio_data = self.sample_portfolio_data.copy()
        original_portfolio_data['name'] = 'modified_1'
        original_portfolio_data['workspace'] = 'modified_1'
        original_portfolio = Portfolio(**original_portfolio_data)

        sample_portfolio_data = self.sample_portfolio_data.copy()
        sample_portfolio_data['id'] = 'port_1234567891011211234567891'
        sample_portfolio_data['name'] = 'modified_2'
        sample_portfolio_data['workspace'] = 'modified_2'
        modified_portfolio = Portfolio(**sample_portfolio_data)

        entity_id_list = [original_portfolio['id'], sample_portfolio_data['id']]

        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = [original_portfolio_data, sample_portfolio_data]
            result = Portfolio.clone_many(entity_id_list=entity_id_list, overwrites=[{'name': 'modified_1'}, {'name': 'modified_1'}])

        mock_http_connection.assert_any_call(class_name='Portfolio', params={'entity_id_list': entity_id_list, 'overwrites': [{'name': 'modified_1'}, {'name': 'modified_1'}]}, method_name='clone_many', self_obj=None)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertIsInstance(result, list)
        self.assertEqual(result[0], original_portfolio)
        self.assertEqual(result[1], modified_portfolio)
        self.assertIsInstance(result[0], Portfolio)
        self.assertIsInstance(result[1], Portfolio)

    def test_save(self):
        portfolio = Portfolio(**self.sample_portfolio_data)
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = self.sample_portfolio_data
            result = portfolio.save()

        mock_http_connection.assert_any_call(class_name='Portfolio', params={}, method_name='save', self_obj=self.sample_portfolio_data)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertEqual(result, self.portfolio)
        self.assertIsInstance(result, Portfolio)

    def test_delete(self):
        portfolio = Portfolio(**self.sample_portfolio_data)
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = self.sample_portfolio_data
            result = portfolio.delete()

        mock_http_connection.assert_any_call(class_name='Portfolio', params={}, method_name='delete', self_obj=self.sample_portfolio_data)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertEqual(result, self.portfolio)
        self.assertIsInstance(result, Portfolio)

    def test_delete_return_none(self):
        portfolio = Portfolio(**self.sample_portfolio_data)
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = None
            result = portfolio.delete()

        mock_http_connection.assert_any_call(class_name='Portfolio', params={}, method_name='delete', self_obj=self.sample_portfolio_data)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertIsNone(result)
