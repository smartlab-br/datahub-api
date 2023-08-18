'''Main tests in API'''
import unittest
from model.source.base import BaseSource

class BaseSourceGetOptionsEmpresaTest(unittest.TestCase):
    ''' Class that tests translation of options from general to
        datasource-oriented ones '''
    OPTIONS = {'cnpj': '12345678000101', 'id_pf': '12345678900'}
    LOCAL_COLS = {
        'cnpj_raiz_flag': 'flag', 'cnpj': 'cnpj_col',
        'cnpj_flag': 'flag_2', 'pf': 'pf_col'
    }
    EXPECTED = [
        "and", "eq-flag-'1'",
        "and", "eq-cnpj_col-12345678000101",
        "and", "eq-flag_2-'1'",
        "and", "eq-pf_col-12345678900"
    ]

    def test_translation(self):
        ''' Tests if the options are correctly built according to given args '''
        self.assertEqual(
            BaseSource().get_options_empresa(
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
                    "eq-cast(col_cnpj_raiz as INT)-12345678",
                    "and", "eq-cast(col_compet as INT)-2099",
                    "and", "eq-flag-'1'",
                    "and", "eq-cnpj_col-12345678000101",
                    "and", "eq-flag_2-'1'",
                    "and", "eq-pf_col-12345678900"
                ],
                'theme': 'theme'
            }
        )

    def test_context_options_empresa(self):
        ''' Tests if the contextual options are correctly built according
            to given args '''
        self.assertEqual(
            BaseSource().get_context_options_empresa(
                self.OPTIONS,
                self.LOCAL_COLS,
                None
            ),
            self.EXPECTED
        )

    def test_context_options_empresa_empty_options(self):
        ''' Tests if the contextual options are correctly built according
            to given args '''
        self.assertEqual(BaseSource().get_context_options_empresa({}, {}, None), [])

    def test_options_rules_empresa(self):
        ''' Tests if the contextual options are correctly built according
            to given args '''
        self.assertEqual(
            BaseSource().get_options_rules_empresa(
                self.OPTIONS,
                self.LOCAL_COLS,
                None,
                None
            ),
            self.EXPECTED
        )
