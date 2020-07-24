'''Main tests in API'''
import unittest
from model.source.rais import Rais

class RaisGetOptionsEmpresaTest(unittest.TestCase):
    ''' Class that tests translation of options from general to
        datasource-oriented ones '''
    def test_rules_empresa_translation(self):
        ''' Tests if the rules are correctly built according to given args '''
        self.assertEqual(
            Rais().get_options_rules_empresa(
                {'column': 2099, 'cnpj_raiz': '12345678'},
                {'compet': 'col_compet', 'cnpj_raiz': 'col_cnpj'},
                'rais',
                None
            ),
            ["and", f"eq-tp_estab-1", "and", "eq-col_compet-2099"]
        )

    def test_rules_empresa_translation_no_compet(self):
        ''' Tests if the rules are correctly built according to given args
            when no timeframe is set '''
        self.assertEqual(
            Rais().get_options_rules_empresa(
                {'cnpj_raiz': '12345678'},
                {'cnpj_raiz': 'col_cnpj'},
                'rais',
                None
            ),
            ["and", f"eq-tp_estab-1"]
        )
