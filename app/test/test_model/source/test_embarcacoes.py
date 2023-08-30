'''Main tests in API'''
import unittest
from model.source.embarcacoes import Embarcacoes

class EmbarcacoesGetOptionsEmpresaTest(unittest.TestCase):
    ''' Class that tests translation of options from general to
        datasource-oriented ones '''
    def test_translation(self):
        ''' Tests if the options are correctly built according to given args '''
        self.assertEqual(
            Embarcacoes().get_options_empresa(
                {'cnpj_raiz': '12345678'},
                {'cnpj_raiz': 'col_cnpj_raiz', 'cnpj': 'col_cnpj'},
                'embarcacoes',
                None
            ),
            {
                'categorias': ['col_cnpj_raiz'],
                'agregacao': ['count'],
                'where': ["eq-cast(col_cnpj_raiz as INT)-12345678",
                          "and", "ne-col_cnpj-'00000000000000'"],
                'theme': 'embarcacoes'
            }
        )
