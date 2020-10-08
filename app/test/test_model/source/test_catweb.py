'''Main tests in API'''
import unittest
from model.source.catweb import Catweb

class CatwebGetOptionsEmpresaTest(unittest.TestCase):
    ''' Class that tests translation of options from general to
        datasource-oriented ones '''
    OPTIONS = {'column': 2099, 'cnpj_raiz': '12345678'}
    LOCAL_COLS = {'compet': 'col_compet', 'cnpj_raiz': 'col_cnpj'}

    def test_options_empresa_translation(self):
        ''' Tests if the options are correctly built according to given args '''
        self.assertEqual(
            Catweb().get_options_empresa(self.OPTIONS, self.LOCAL_COLS, 'catweb', None),
            {
                'categorias': ['col_cnpj'],
                'agregacao': ['count'],
                'where': [
                    "eq-col_cnpj-'12345678'",
                    "and", "ge-col_compet-\'20990101\'",
                    "and", "le-col_compet-\'20991231\'"
                ],
                'theme': 'catweb_c'}
        )

    def test_rules_empresa_translation(self):
        ''' Tests if the rules are correctly built according to given args '''
        self.assertEqual(
            Catweb().get_options_rules_empresa(self.OPTIONS, self.LOCAL_COLS, 'catweb', None),
            [
                "and", f"ge-col_compet-\'20990101\'",
                "and", f"le-col_compet-\'20991231\'"
            ]
        )
