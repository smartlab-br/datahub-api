'''Main tests in API'''
import unittest
from model.source.caged import BaseCaged, CagedSaldo

class BaseCagedGetOptionsEmpresaTest(unittest.TestCase):
    ''' Class that tests translation of options from general to
        datasource-oriented ones '''
    def test_options_empresa_translation(self):
        ''' Tests if the options are correctly built according to given args '''
        self.assertEqual(
            BaseCaged().get_options_empresa(
                {'column': 2099, 'cnpj_raiz': '12345678'},
                {'compet': 'col_compet', 'cnpj_raiz': 'col_cnpj_raiz'},
                'cagedtrabalhador',
                None
            ),
            {
                'categorias': ['col_cnpj_raiz'],
                'agregacao': ['count'],
                'where': [
                    "eq-cast(col_cnpj_raiz as INT)-12345678",
                    "and", "eq-tipo_estab-1",
                    "and", "eq-cast(col_compet as INT)-2099"
                ],
                'theme': 'cagedtrabalhador'
            }
        )

    def test_rules_empresa_translation(self):
        ''' Tests if the options are correctly built according to given args '''
        self.assertEqual(
            BaseCaged().get_options_rules_empresa(
                {'column': 2099, 'cnpj_raiz': '12345678'},
                {'compet': 'col_compet', 'cnpj_raiz': 'col_cnpj_raiz'},
                'caged',
                None
            ),
            ["and", "eq-tipo_estab-1", "and", "eq-col_compet-2099"]
        )

    def test_rules_empresa_translation_no_compet(self):
        ''' Tests if the options are correctly built according to given args
            when no timeframe is set '''
        self.assertEqual(
            BaseCaged().get_options_rules_empresa(
                {'cnpj_raiz': '12345678'},
                {'cnpj_raiz': 'col_cnpj_raiz'},
                'caged',
                None
            ),
            ["and", "eq-tipo_estab-1"]
        )

class CagedSaldoGetOptionsEmpresaTest(unittest.TestCase):
    ''' Class that tests translation of options from general to
        datasource-oriented ones '''
    def test_options_empresa_translation(self):
        ''' Tests if the options are correctly built according to given args '''
        self.assertEqual(
            CagedSaldo().get_options_empresa(
                {'cnpj_raiz': '12345678'},
                {'cnpj_raiz': 'col_cnpj_raiz'},
                'cagedsaldo',
                None
            ),
            {
                'categorias': ['\'1\'-pos'],
                "valor": ['qtd_admissoes', 'qtd_desligamentos', 'saldo_mov'],
                'agregacao': ['sum'],
                'where': [
                    "eqlpint-col_cnpj_raiz-12345678-14-0-1-8",
                    "and", "eq-tipo_estab-1"
                ],
                'theme': 'cagedsaldo'
            }
        )
