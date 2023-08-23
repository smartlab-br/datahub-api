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
                {'cnpj': 'col_cnpj', 'cnpj_raiz': 'col_cnpj_raiz'},
                'aeronaves',
                None
            ),
            {
                'categorias': ['col_cnpj_raiz'],
                'agregacao': ['count'],
                'where': [
                    "eq-cast(col_cnpj_raiz as INT)-12345678", 
                    "and", "ne-cast(col_cnpj as INT)-0"
                ],
                'theme': 'aeronaves'
            }
        )
