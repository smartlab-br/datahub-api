'''Main tests in API'''
import unittest
from datetime import datetime
from model.empresa.empresa import Empresa
from test.stubs.empresa import StubEmpresa
from test.stubs.empresa import StubDatasetRepository

class EmpresaModelBaseTest(unittest.TestCase):
    ''' Classe que testa o mapeamento de agregações para funções do pandas '''
    def test_default_on_none(self):
        ''' Verifica se retorna np.mean se agregação nula '''
        self.assertEqual(
            StubEmpresa().get_stats_local_options(
                {
                    'column': 2099,
                    'cnpj_raiz': '12345678',
                    'cnpj': '12345678000101',
                    'id_pf': '12345678900'
                },
                {
                    'compet': 'col_compet',
                    'cnpj_raiz': 'col_cnpj_raiz',
                    'cnpj_raiz_flag': 'flag', 'cnpj': 'cnpj_col',
                    'cnpj_flag': 'flag_2', 'pf': 'pf_col'
                },
                'theme',
                None
            ),
            {
                'categorias': ['col_cnpj_raiz'],
                'agregacao': ['count'],
                'where': [
                    "eq-col_cnpj_raiz-12345678",
                    "and", "eq-flag-'1'",
                    "and", "eq-cnpj_col-12345678000101",
                    "and", "eq-flag_2-'1'",
                    "and", "eq-pf_col-12345678900"
                ],
                'theme': 'theme'
            }
        )

    def test_build_empty_stats_no_aggr(self):
        ''' Tests if a 0 total object is created according to given options with
            no aggregations '''
        self.assertEqual(
            Empresa.build_empty_stats(
                {},
                {"cnpj_raiz": "col_cnpj_raiz"},
                {"cnpj_raiz": "12345678"}
            ),
            {"col_cnpj_raiz": "12345678"}
        )

    def test_build_empty_stats_aggr(self):
        ''' Tests if a 0 total object is created according to given options with
            aggregations '''
        self.assertEqual(
            Empresa.build_empty_stats(
                {"agregacao": ['sum', 'count']},
                {"cnpj_raiz": "col_cnpj_raiz"},
                {"cnpj_raiz": "12345678"}
            ),
            {
                "col_cnpj_raiz": "12345678",
                "agr_sum": 0,
                "agr_count": 0
            }
        )

    def test_build_empty_stats_val_aggr(self):
        ''' Tests if a 0 total object is created according to given options with
            aggregations and values '''
        self.assertEqual(
            Empresa.build_empty_stats(
                {"agregacao": ['sum', 'count'], "valor": ['vl_a', 'vl_b']},
                {"cnpj_raiz": "col_cnpj_raiz"},
                {"cnpj_raiz": "12345678"}
            ),
            {
                "col_cnpj_raiz": "12345678",
                "agr_sum_vl_a": 0, "agr_count_vl_a": 0,
                "agr_sum_vl_b": 0, "agr_count_vl_b": 0
            }
        )

class AssessColumnStatusTest(unittest.TestCase):
    ''' Class to test the status assessmente from a collection of status
        keys retrieved from REDIS '''
    SLOT_LIST = ['2019', '2020', '2047']
    KEY_COLLECTION = {'2019': 'INGESTED', '2020': 'INGESTING', '2099': 'INGESTED'}

    def test_assess_column_status_existing(self):
        ''' Tests if the existing column status is returned correctly '''
        self.assertEqual(
            Empresa.assess_column_status(self.SLOT_LIST, self.KEY_COLLECTION, '2019'),
            'INGESTED'
        )

    def test_assess_column_status_missing(self):
        ''' Tests if the missing column status is returned correctly when
            the column exists in the list but not in the collection from REDIS '''
        self.assertEqual(
            Empresa.assess_column_status(self.SLOT_LIST, self.KEY_COLLECTION, '2047'),
            'MISSING'
        )

    def test_assess_column_status_deprecated(self):
        ''' Tests if the deprecated data status is returned correctly when
            the column exists in the collection from REDIS but not in the
            dictionary of data present in datalake '''
        self.assertEqual(
            Empresa.assess_column_status(self.SLOT_LIST, self.KEY_COLLECTION, '2099'),
            'DEPRECATED'
        )

    def test_assess_column_status_unavailable(self):
        ''' Tests if the unavailable column status is returned correctly
            when a data that is not present both in the dictionary of
            available data and the REDIS collection '''
        self.assertEqual(
            Empresa.assess_column_status(self.SLOT_LIST, self.KEY_COLLECTION, '1500'),
            'UNAVAILABLE'
        )

class StubGetGroupedStatsTest(unittest.TestCase):
    ''' Tests the grouped statistics fetching using static data as source '''
    def test_get_grouped_stats(self):
        ''' Tests basic grouped stats retrieval '''
        self.assertEqual(
            StubEmpresa().get_grouped_stats(
                {},
                {'theme': 'mytheme'},
                {'compet': 'compet'}
            ),
            {
                'stats_estab': {
                    '12345678000101': {'agr_count': 100, 'compet': 2047},
                    '12345678000202': {'agr_count': 200, 'compet': 2099}
                },
                'stats_compet': {
                    '2047': {'agr_count': 100, 'cnpj': '12345678000101'},
                    '2099': {'agr_count': 200, 'cnpj': '12345678000202'}
                },
                'stats_estab_compet': {
                    '2047_12345678000101': {
                        'agr_count': 100, 'cnpj': '12345678000101', 'compet': 2047
                    },
                    '2099_12345678000202': {
                        'agr_count': 200, 'cnpj': '12345678000202', 'compet': 2099
                    }
                }
            }
        )

    def test_get_grouped_stats_displaced_compet_alt(self):
        ''' Tests basic grouped stats retrieval '''
        self.assertEqual(
            StubEmpresa().get_grouped_stats(
                {},
                {'theme': 'catewb'},
                {}
            ),
            StubEmpresa.EXPECTED_GROUPED_STATS
        )

class StubGetStatisticsFromPerspectiveTest(unittest.TestCase):
    ''' Tests the grouped perspective statistics fetching using static
        data as source '''
    def test_get_statistic_from_perspective(self):
        ''' Tests basic grouped perspective stats retrieval
            when no perspective is given '''
        self.assertEqual(
            StubEmpresa().get_statistics_from_perspective(
                'mytheme', None, {}, 
                {"categorias": ['cnpj']},
                {"categorias": ['cnpj']}
            ),
            {
                **{
                    'fonte': 'Fonte',
                    'stats': {'cnpj': '12345678000101', 'compet': 2047, 'agr_count': 100}
                },
                **StubEmpresa.EXPECTED_GROUPED_STATS
            }
        )

    def test_get_statistic_from_perspective_perspective(self):
        ''' Tests basic grouped perspective stats retrieval '''
        self.assertEqual(
            StubEmpresa().get_statistics_from_perspective(
                'mytheme', 'mypersp', {}, 
                {"categorias": ['cnpj'], 'where': []},
                {"categorias": ['cnpj']}
            ),
            {
                **{
                    'stats': {'cnpj': '12345678000101', 'compet': 2047, 'agr_count': 100}
                },
                **StubEmpresa.EXPECTED_GROUPED_STATS
            }
        )

class StubGetStatisticsTest(unittest.TestCase):
    ''' Tests the grouped perspective statistics fetching using static
        data as source '''
    def test_get_statistic_column_family_no_perspective_no_timeframe(self):
        ''' Tests statistics retrieval for a specific dataset with no
            perspective and timeframe definition '''
        self.assertEqual(
            StubEmpresa().get_statistics({
                "cnpj_raiz": '12345678',
                "theme": 'rfb',
                "column_family": "rfb",
                "categorias": ['cnpj']
            }),
            {
                "rfb": {
                    'fonte': 'Fonte',
                    'stats': {'cnpj': '12345678000101', 'compet': 2047, 'agr_count': 100}
                }
            }
        )

    def test_get_statistic_column_family_no_perspective(self):
        ''' Tests statistics retrieval for a specific dataset with no
            perspective definition, but an existing timeframe rule '''
        self.assertEqual(
            StubEmpresa().get_statistics({
                "cnpj_raiz": '12345678',
                "theme": 'rais',
                "column_family": "rais",
                "categorias": ['nu_cnpj_cei']
            }),
            {
                "rais": {
                    'fonte': 'Fonte',
                    'stats': {'nu_cnpj_cei': '12345678000101', 'nu_ano_rais': 2047, 'agr_count': 100},
                    'stats_estab': {
                        '12345678000101': {'agr_count': 100, 'nu_ano_rais': 2047},
                        '12345678000202': {'agr_count': 200, 'nu_ano_rais': 2099}
                    },
                    'stats_compet': {
                        '2047': {'agr_count': 100, 'nu_cnpj_cei': '12345678000101'},
                        '2099': {'agr_count': 200, 'nu_cnpj_cei': '12345678000202'}
                    },
                    'stats_estab_compet': {
                        '2047_12345678000101': {
                            'agr_count': 100, 'nu_cnpj_cei': '12345678000101', 'nu_ano_rais': 2047
                        },
                        '2099_12345678000202': {
                            'agr_count': 200, 'nu_cnpj_cei': '12345678000202', 'nu_ano_rais': 2099
                        }
                    }
                }
            }
        )

    # def test_get_statistic_column_family_with_perspective_no_timeframe(self):
    #     ''' Tests statistics retrieval for a specific dataset with no
    #         timeframe definition, but an existing perspective rule '''
    #     self.assertEqual(
    #         StubEmpresa().get_statistics({
    #             "theme": 'mytheme',
    #             "column_family": "rais",
    #             "perspective": 'mypersp',
    #             "categorias": ['cnpj'],
    #             'where': []
    #         }),
    #         {
    #             **{
    #                 'stats': {'cnpj': '12345678000101', 'compet': 2047, 'agr_count': 100}
    #             },
    #             **StubEmpresa.EXPECTED_GROUPED_STATS
    #         }
    #     )

    # def test_get_statistic_column_family_with_perspective(self):
    #     ''' Tests statistics retrieval for a specific dataset with
    #         perspective and timeframe definitions '''
    #     self.assertEqual(
    #         StubEmpresa().get_statistics({
    #             "theme": 'catweb',
    #             "column_family": "catweb",
    #             "perspective": 'empregador',
    #             "categorias": ['cnpj'],
    #             "column": '2047',
    #             'where': []
    #         }),
    #         {
    #             "catweb": {
    #                 'stats_persp': {
    #                     'empregador': {
    #                         'stats': {
    #                             'agr_count': 100,
    #                             'cnpj': '12345678000101',
    #                             'cnpj_raiz': '12345678',
    #                             'compet': 2047,
    #                             'nu_cnpj_empregador': '12345678000101',
    #                             'tp_tomador': 0
    #                         },
    #                         'stats_estab': {
    #                             '12345678000101': {
    #                                 'agr_count': 100, 'compet': 2047,
    #                                 'cnpj': '12345678000101',
    #                                 'cnpj_raiz': '12345678', 'tp_tomador': 0
    #                             },
    #                             '12345678000202': {
    #                                 'agr_count': 200, 'compet': 2047,
    #                                 'cnpj': '12345678000202',
    #                                 'cnpj_raiz': '12345678', 'tp_tomador': 0
    #                             }
    #                         },
    #                         'stats_compet': {
    #                             '2047': {
    #                                 'cnpj': '12345678000202',
    #                                 'agr_count': 200,
    #                                 'nu_cnpj_empregador': '12345678000202',
    #                                 'cnpj_raiz': '12345678', 'tp_tomador': 0
    #                             },
    #                         },
    #                         'stats_estab_compet': {
    #                             '2047_12345678000101': {
    #                                 'cnpj': '12345678000101',
    #                                 'agr_count': 100, 'compet': 2047,
    #                                 'nu_cnpj_empregador': '12345678000101',
    #                                 'cnpj_raiz': '12345678', 'tp_tomador': 0
    #                             },
    #                             '2047_12345678000202': {
    #                                 'cnpj': '12345678000202',
    #                                 'agr_count': 200, 'compet': 2047,
    #                                 'nu_cnpj_empregador': '12345678000202',
    #                                 'cnpj_raiz': '12345678', 'tp_tomador': 0
    #                             }
    #                         }
    #                     }
    #                 }
    #             }
    #         }
    #     )

    def test_get_statistic_column_family_with_perspective_invalid_value(self):
        ''' Tests statistics retrieval for a specific dataset with
            perspective and timeframe definitions '''
        self.assertRaises(
            AttributeError,
            StubEmpresa().get_statistics,
            {
                "theme": 'catweb',
                "column_family": "catweb",
                "perspective": 'invalid',
                "categorias": ['cnpj'],
                "column": '2047',
                'where': []
            }
        )
    
    # def test_get_statistic_overall(self):
    #     ''' Tests basic grouped perspective stats retrieval '''
    #     self.assertEqual(
    #         StubEmpresa().get_statistics({
    #             "categorias": ['cnpj'],
    #             "column": '2099',
    #             'where': []
    #         }),
    #         {
    #             **{
    #                 'stats': {'cnpj': '12345678000101', 'compet': 2047, 'agr_count': 100}
    #             },
    #             **StubEmpresa.EXPECTED_GROUPED_STATS
    #         }
    #     )

    def test_get_statistic_overall_timeframe_validation(self):
        ''' Tests if timeframe requirement is forced on overall request '''
        self.assertRaises(
            AttributeError,
            StubEmpresa().get_statistics,
            {
                "categorias": ['cnpj'],
                'where': []
            }
        )

    def test_get_statistic_raise_on_timeframe_validation_error(self):
        ''' Tests if timeframe requirement is forced '''
        self.assertRaises(
            AttributeError,
            StubEmpresa().get_statistics,
            {
                "theme": "auto",
                "column_family": "auto",
                "categorias": ['cnpj'],
                'where': []
            }
        )

class StubGetIsValidLoadingEntryTest(unittest.TestCase):
    ''' Tests the loading entry validation method '''
    def test_is_valid_loading_entry_no_options(self):
        ''' Tests if error is raised when no options is given '''
        self.assertRaises(
            ValueError,
            StubEmpresa().is_valid_loading_entry,
            '12345678',
            None
        )

    def test_is_valid_loading_entry_no_column_family(self):
        ''' Tests if error is raised when no column family is given '''
        self.assertRaises(
            ValueError,
            StubEmpresa().is_valid_loading_entry,
            '12345678',
            {}
        )

    def test_is_valid_loading_entry_wrong_column_family(self):
        ''' Tests if error is raised when an incorrect column family is given '''
        self.assertRaises(
            ValueError,
            StubEmpresa().is_valid_loading_entry,
            '12345678',
            {'column_family': 'non-existent'},
            StubDatasetRepository.DATASETS
        )

    def test_is_valid_loading_entry_wrong_column(self):
        ''' Tests if error is raised when an incorrect column is given
            to filter the data from a row '''
        self.assertRaises(
            ValueError,
            StubEmpresa().is_valid_loading_entry,
            '12345678',
            {'column_family': 'test', 'column': '2099'},
            StubDatasetRepository.DATASETS
        )

    def test_is_valid_loading_entry(self):
        ''' Tests if validation passes whe no falseability conditions are
            met '''
        self.assertEqual(
            StubEmpresa().is_valid_loading_entry(
                '12345678',
                {'column_family': 'test', 'column': '2017'},
                StubDatasetRepository.DATASETS
            ),
            True
        )

    def test_is_valid_loading_entry_false_column(self):
        ''' Tests if validation fails when the requires column is not in the
            available list '''
        self.assertEqual(
            StubEmpresa().is_valid_loading_entry(
                '12345678',
                {'column_family': 'another'},
                StubDatasetRepository.DATASETS
            ),
            False
        )

    # def test_is_valid_loading_entry_false_by_status(self):
    #     ''' Tests if validation fails '''
    #     self.assertEqual(
    #         StubEmpresa().is_valid_loading_entry(
    #             '12345678',
    #             {'column_family': 'failed_status', 'column': '2017'},
    #             StubDatasetRepository.DATASETS
    #         ),
    #         False
    #     )

    def test_is_valid_loading_entry_false_expired(self):
        ''' Tests if validation fails '''
        self.assertEqual(
            StubEmpresa().is_valid_loading_entry(
                '12345678',
                {'column_family': 'expired', 'column': '2018'},
                StubDatasetRepository.DATASETS
            ),
            False
        )

class StubGetLoadingEntryTest(unittest.TestCase):
    ''' Tests the loading entry validation method '''
    EXPECTED = {
        "2017": f'INGESTED|{datetime.strftime(datetime.now(), "%Y-%m-%d")}',
        "2018": f'INGESTED|{datetime.strftime(datetime.now(), "%Y-%m-%d")}',
        "when": f'{datetime.strftime(datetime.now(), "%Y-%m-%d")}'
    }

    def get_expected_status_dict(self):
        ''' Method to avoid duplicate code for default test expected dictionary '''
        return {
            "another": self.EXPECTED,
            "expired": {
                "2017": "INGESTED|2000-01-01",
                "2018": "INGESTED|2000-01-01",
                "when": "2000-01-01"
            },
            "failed_status": {
                "2017": f'FAILED|{datetime.strftime(datetime.now(), "%Y-%m-%d")}',
                "2018": f'INGESTED|{datetime.strftime(datetime.now(), "%Y-%m-%d")}',
                "when": f'{datetime.strftime(datetime.now(), "%Y-%m-%d")}'
            },
            "skip": self.EXPECTED,
            "test": self.EXPECTED
        }

    def test_get_loading_entry_no_options(self):
        ''' Tests if no column status is returned when no options is given '''
        self.assertEqual(
            StubEmpresa().get_loading_entry('12345678', None, StubDatasetRepository.DATASETS),
            (
                self.get_expected_status_dict(),
                None
            )
        )

    def test_get_loading_entry_empty_options(self):
        ''' Tests if no column status is returned when an empty options is given '''
        self.assertEqual(
            StubEmpresa().get_loading_entry('12345678', {}, StubDatasetRepository.DATASETS),
            (
                self.get_expected_status_dict(),
                None
            )
        )

    def test_valid_loading_entry(self):
        ''' Tests return of valid ingested loading entry '''
        self.assertEqual(
            StubEmpresa().get_loading_entry(
                '12345678',
                {'column_family': 'test', 'column': '2017'},
                StubDatasetRepository.DATASETS
            ),
            (
                self.get_expected_status_dict(),
                f'INGESTED|{datetime.strftime(datetime.now(), "%Y-%m-%d")}'
            )
        )

    def test_valid_loading_entry_no_column_in_options(self):
        ''' Tests return of valid loading entry when no column is given '''
        self.assertEqual(
            StubEmpresa().get_loading_entry(
                '12345678',
                {'column_family': 'failed_status'},
                StubDatasetRepository.DATASETS
            ),
            (
                self.get_expected_status_dict(),
                None
            )
        )

class StubAssessColumnStatusTest(unittest.TestCase):
    ''' Tests the column status assessor '''
    def test_assess_column_status_no_column_args(self):
        ''' Tests if UNAVAILABLE is returned when no column args are provided '''
        self.assertEqual(
            StubEmpresa.assess_column_status(
                ['2017', '2018'],
                None,
                None
            ),
            'UNAVAILABLE'
        )

    def test_assess_column_status_empty_available_column_arg(self):
        ''' Tests if UNAVAILABLE is returned when no column and an empty
            columns_available args are provided '''
        self.assertEqual(
            StubEmpresa.assess_column_status(
                ['2017', '2018'],
                {},
                None
            ),
            'UNAVAILABLE'
        )

    def test_assess_column_status_missing(self):
        ''' Tests if MISSING is returned when a given column is expected but
            not present in the columns_available (from REDIS) '''
        self.assertEqual(
            StubEmpresa.assess_column_status(
                ['2017', '2018'],
                {"2017": 'INGESTED'},
                '2018'
            ),
            'MISSING'
        )

    def test_assess_column_status_deprecated(self):
        ''' Tests if MISSING is returned when a given column is not expected
            (removed from the datalake reference, but is retrieved from REDIS '''
        self.assertEqual(
            StubEmpresa.assess_column_status(
                ['2017', '2018'],
                {"2019": 'INGESTED'},
                '2019'
            ),
            'DEPRECATED'
        )

    def test_assess_column_status_unavailable_deprecated_not_ingested(self):
        ''' Tests if MISSING is returned when a given column is not expected
            (removed from the datalake reference, but is retrieved from REDIS
            with a non-INGESTED status '''
        self.assertEqual(
            StubEmpresa.assess_column_status(
                ['2017', '2018'],
                {"2019": 'FAILED|2000-01-01'},
                '2019'
            ),
            'UNAVAILABLE'
        )

    def test_assess_column_status_from_data(self):
        ''' Tests if a regular status is passed AS-IS if guard conditions
            are not met '''
        self.assertEqual(
            StubEmpresa.assess_column_status(
                ['2017', '2018'],
                {"2018": 'FAILED|2000-01-01'},
                '2018'
            ),
            'FAILED|2000-01-01'
        )
