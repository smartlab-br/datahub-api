'''Main tests in API'''
import unittest
from model.source.aeronaves import Aeronaves

class AeronavesGetOptionsEmpresaTest(unittest.TestCase):
    ''' Class that tests translation of options from general to
        datasource-oriented ones '''
    def test_translation(self):
        ''' Tests if the options are correctly built according to given args '''
        self.assertEqual(
            Aeronaves().get_options_empresa(
                {'cnpj_raiz': '12345678'},
                {'cnpj_raiz': 'col_cnpj'},
                'aeronaves',
                None
            ),
            {
                'categorias': ['col_cnpj'],
                'agregacao': ['count'],
                'where': ['eqon-col_cnpj-12345678-1-8', 'and', 'neon-col_cnpj-00000000000000'],
                'theme': 'aeronaves'
            }
        )
