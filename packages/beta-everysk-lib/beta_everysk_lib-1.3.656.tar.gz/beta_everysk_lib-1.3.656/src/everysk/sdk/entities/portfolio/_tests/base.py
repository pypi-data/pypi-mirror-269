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

from everysk.core.datetime import DateTime, Date

from everysk.sdk.entities.portfolio.base import SecuritiesField, Portfolio
from everysk.sdk.entities.portfolio.securities import Securities
from everysk.sdk.entities.portfolio.security import Security

###############################################################################
#   Securities Field TestCase Implementation
###############################################################################
class TestSecuritiesField(TestCase):

    def setUp(self):
        self.securities_field = SecuritiesField()

    def test_clean_value_with_list(self):
        test_value = [{"symbol": "AAPL", "name": "Apple Inc."}]
        cleaned_value = self.securities_field.clean_value(test_value)

        # Ensure the cleaned value is of type `Securities`
        self.assertIsInstance(cleaned_value, Securities)

    def test_clean_value_without_list(self):
        test_value = "Some value"
        cleaned_value = self.securities_field.clean_value(test_value)

        # Ensure the cleaned value is not modified
        self.assertEqual(cleaned_value, [test_value])

###############################################################################
#   Portfolio TestCase Implementation
###############################################################################
class TestPortfolio(TestCase):

    def setUp(self):
        self.sample_data = {
            'id': 'port_1234567891011211234567890',
            'workspace': 'SampleWorkspace',
            'name': 'SamplePortfolio',
            'tags': ['tag1', 'tag2'],
            'link_uid': 'ABC',
            'description': 'Description',
            'nlv': 1000.0,
            'base_currency': 'USD',
            'date': DateTime(2023, 9, 9, 9, 9, 9, 9),
            'securities': Securities([{'symbol': 'AAPL'}]),
            'version': '1.0',
            'created_on': DateTime(2023, 9, 9, 9, 9, 9, 9),
            'updated_on': DateTime(2023, 9, 9, 9, 9, 9, 9),
            'level': 'v1',
            'outstanding_shares': 1000,
            'source_hash': 'XYZ',
            'status': 'OK',
            'portfolio_uid': 'UID123',
            'check_securities': False
        }
        self.portfolio = Portfolio(**self.sample_data)

    def test_static_methods(self):
        self.assertEqual(Portfolio.get_id_prefix(), settings.PORTFOLIO_ID_PREFIX)

    def test_validate(self):
        portfolio: Portfolio = self.portfolio.copy()
        portfolio.check_securities = True
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = True
            result = portfolio.validate()

        mock_http_connection.assert_called_once_with(class_name='Portfolio', params={}, method_name='validate', self_obj=portfolio)
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertTrue(result)

    def test_to_dict(self):
        dict_output = self.portfolio.to_dict()
        self.assertIsInstance(dict_output, dict)
        self.assertEqual(dict_output['name'], self.sample_data['name'])
        self.assertEqual(dict_output['date'], Date.strftime_or_null(self.sample_data['date']))
        self.assertEqual(dict_output['created'], self.sample_data['created_on'].timestamp())

    def test_check(self):
        entity_dict = self.sample_data.copy()
        entity_dict['check_securities'] = True
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = self.sample_data
            result = Portfolio.check(entity_dict=entity_dict)

        mock_http_connection.assert_any_call(class_name='Portfolio', params={}, method_name='validate', self_obj=entity_dict)
        mock_http_connection.return_value.get_response.assert_called_once_with()

        check_port = self.portfolio.copy()
        check_port.check_securities = True
        self.assertEqual(result, check_port)
        self.assertIsInstance(result, Portfolio)

    def test_to_csv(self):
        out_csv = self.portfolio.to_csv()
        self.assertIsInstance(out_csv, str)

    def test_to_dict_without_internals(self):
        dict_output = self.portfolio.to_dict(with_internals=False)
        self.assertIsInstance(dict_output, dict)
        self.assertEqual(dict_output['securities'][0], Security(symbol='AAPL').to_dict(with_internals=False))

    def test_to_dict_no_modify_obj_by_reference(self):
        portfolio = Portfolio(
            date=DateTime(2021, 1, 1, 1, 1, 1),
            created_on=DateTime(2021, 1, 1, 1, 1, 1),
            updated_on=DateTime(2021, 1, 1, 1, 1, 1),
            tags=['tag1', 'tag2'],
            securities=[{
                'symbol': 'AAPL',
                'maturation_date': Date(2021, 1, 1),
                'extra_data': {
                    'date': Date(2021, 1, 1),
                    'datetime': DateTime(2021, 1, 1, 1, 1, 1),
                    'date_list': [Date(2021, 1, 1)],
                    'datetime_list': [DateTime(2021, 1, 1, 1, 1, 1)],
                    'dict': {'a': 1, 'b': 2},
                    'tuple_list': [(Date(2021, 1, 1),)],
                    'date_tuple': (Date(2021, 1, 1),),
                    'date_set': set([Date(2021, 1, 1)])
                }}])
        dict_output = portfolio.to_dict(with_internals=False)

        self.assertDictEqual(
            dict_output,
            {
                'id': None,
                'workspace': None,
                'name': None,
                'tags': ['tag1', 'tag2'],
                'link_uid': None,
                'description': None,
                'nlv': None,
                'base_currency': None,
                'date': '20210101',
                'securities': [
                    {
                        'status': None,
                        'id': None,
                        'symbol': 'AAPL',
                        'quantity': None,
                        'instrument_class': None,
                        'ticker': None,
                        'label': None,
                        'name': None,
                        'isin': None,
                        'exchange': None,
                        'currency': None,
                        'fx_rate': None,
                        'market_price': None,
                        'premium': None,
                        'market_value': None,
                        'market_value_in_base': None,
                        'instrument_type': None,
                        'instrument_subtype': None,
                        'asset_class': None,
                        'asset_subclass': None,
                        'error_type': None,
                        'error_message': None,
                        'maturity_date': None,
                        'indexer': None,
                        'percent_index': None,
                        'rate': None,
                        'coupon': None,
                        'multiplier': None,
                        'underlying': None,
                        'series': None,
                        'option_type': None,
                        'strike': None,
                        'issue_price': None,
                        'issue_date': None,
                        'issuer': None,
                        'issuer_type': None,
                        'cost_price': None,
                        'unrealized_pl': None,
                        'unrealized_pl_in_base': None,
                        'book': None,
                        'trader': None,
                        'trade_id': None,
                        'operation': None,
                        'accounting': None,
                        'warranty': None,
                        'return_date': None,
                        'settlement': None,
                        'look_through_reference': None,
                        'extra_data': {
                            'maturation_date': '20210101',
                            'date': '20210101',
                            'datetime': '20210101 01:01:01',
                            'date_list': ['20210101'],
                            'datetime_list': ['20210101 01:01:01'],
                            'dict': {'a': 1, 'b': 2},
                            'tuple_list': [('20210101',)],
                            'date_tuple': ('20210101',),
                            'date_set': ['20210101']
                        },
                        'hash': None
                    }
                ],
                'version': 'v1',
                'level': None,
                'check_securities': False,
                'date_time': '20210101 01:01:01',
                'created': 1609462861,
                'updated': 1609462861
            }
        )

        dict_output['tags'].append('tag3')
        self.assertNotIn('tag3', portfolio.tags)

        dict_output['securities'][0]['extra_data']['date_list'].append('20210102')
        self.assertNotIn('20210102', portfolio.securities[0].extra_data.date_list)

        dict_output['securities'][0]['extra_data']['datetime_list'].append('20210102 01:01:01')
        self.assertNotIn('20210102 01:01:01', portfolio.securities[0].extra_data.datetime_list)

        dict_output['securities'][0]['extra_data']['tuple_list'].append(('20210102',))
        self.assertNotIn(('20210102',), portfolio.securities[0].extra_data.tuple_list)

        dict_output['securities'][0]['extra_data']['date_tuple'] += ('20210102',)
        self.assertNotIn('20210102', portfolio.securities[0].extra_data.date_tuple)

        dict_output['securities'][0]['extra_data']['date_set'].append('20210102')
        self.assertNotIn('20210102', portfolio.securities[0].extra_data.date_set)

        dict_output['securities'][0]['extra_data']['dict']['c'] = 3
        self.assertNotIn('c', portfolio.securities[0].extra_data.dict)

    def test_query_load_with_id(self):
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = self.sample_data
            result = Portfolio(id='port_1234567891011211234567890', workspace='SampleWorkspace').load()

        mock_http_connection.assert_called_once_with(
            params={'entity_id': 'port_1234567891011211234567890'},
            class_name='Portfolio',
            method_name='retrieve',
            self_obj=None
        )
        mock_http_connection.return_value.get_response.assert_called_once_with()

        self.assertEqual(result, self.portfolio)
        self.assertIsInstance(result, Portfolio)

    def test_query_load(self):
        with mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = self.sample_data
            result = Portfolio(link_uid='SampleLinkUID', workspace='SampleWorkspace').load()

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

        self.assertEqual(result, self.portfolio)
        self.assertIsInstance(result, Portfolio)
