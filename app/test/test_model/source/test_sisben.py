'''Main tests in API'''
import unittest
from model.source.sisben import Sisben

class SisbenGetOptionsEmpresaTest(unittest.TestCase):
    ''' Class that tests translation of options from general to
        datasource-oriented ones '''
    def test_options_empresa_translation(self):
        ''' Tests if the options are correctly built according to given args '''
        self.assertEqual(
            Sisben().get_options_empresa(
                {'column': 2099, 'cnpj_raiz': '12345678'},
                {'cnpj': 'col_cnpj', 'cnpj_raiz': 'col_cnpj_raiz'},
                'sisben',
                None
            ),
            {
                'categorias': ['col_cnpj_raiz'],
                'agregacao': ['count'],
                'where': ["eq-col_cnpj_raiz-'12345678'", "and", "ne-col_cnpj-'00000000000000'"],
                'theme': 'sisben_c'}
        )
