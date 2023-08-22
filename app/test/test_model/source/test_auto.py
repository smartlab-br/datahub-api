'''Main tests in API'''
import unittest
from model.source.auto import Auto

class AutoGetOptionsEmpresaTest(unittest.TestCase):
    ''' Class that tests translation of options from general to
        datasource-oriented ones '''
    OPTIONS = {'column': 2099, 'cnpj_raiz': '12345678'}
    LOCAL_COLS = {'compet': 'col_compet', 'cnpj_raiz': 'col_cnpj'}

    def test_options_empresa_translation(self):
        ''' Tests if the options are correctly built according to given args '''
        self.assertEqual(
            Auto().get_options_empresa(self.OPTIONS, self.LOCAL_COLS, 'auto', None),
            {
                'categorias': ['col_cnpj'],
                'agregacao': ['count'],
                'where': [
                    "eq-cast(col_cnpj as INT)-12345678",
                    'and', "eq-cast(col_compet as INT)-2099",
                    'and', "eq-tpinscricao-'1'",
                    'and', 'nl-dtcancelamento'
                ],
                'theme': 'auto'}
        )

    def test_rules_empresa_translation(self):
        ''' Tests if the rules are correctly built according to given args '''
        self.assertEqual(
            Auto().get_options_rules_empresa(self.OPTIONS, self.LOCAL_COLS, 'auto', None),
            [
                'and', "eq-tpinscricao-'1'",
                'and', 'nl-dtcancelamento'
            ]
        )
