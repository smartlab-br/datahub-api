'''Main tests in API'''
import unittest
from model.empresa.empresa import Empresa

class EmpresaModelBaseTest(unittest.TestCase):
    ''' Classe que testa o mapeamento de agregações para funções do pandas '''
    def test_default_on_none(self):
        ''' Verifica se retorna np.mean se agregação nula '''
        self.assertEqual(
            Empresa().get_stats_local_options(
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
