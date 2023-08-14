'''Main tests in API'''
import unittest
from model.source.rfb import BaseRfb, RfbSocios, RfbParticipacaoSocietaria

class BaseRfbGetOptionsEmpresaTest(unittest.TestCase):
    ''' Class that tests translation of options from general to
        datasource-oriented ones '''
    def test_options_empresa_translation(self):
        ''' Tests if the options are correctly built according to given args '''
        self.assertEqual(
            BaseRfb().get_options_empresa(
                {'cnpj_raiz': '12345678'},
                {'cnpj_raiz': 'col_cnpj_raiz'},
                'rfb',
                None
            ),
            {
                'categorias': ['\'1\'-pos'],
                'agregacao': ['count'],
                'where': ["eq-col_cnpj_raiz-12345678"],
                'theme': 'rfb'
            }
        )

class RfbSociosGetOptionsEmpresaTest(unittest.TestCase):
    ''' Class that tests translation of options from general to
        datasource-oriented ones '''
    def test_options_empresa_translation(self):
        ''' Tests if the options are correctly built according to given args '''
        self.assertEqual(
            RfbSocios().get_options_empresa(
                {'cnpj_raiz': '12345678'},
                {'cnpj_raiz': 'col_cnpj_raiz'},
                'rfbsocios',
                None
            ),
            {
                'categorias': ['\'1\'-pos'],
                'agregacao': ['count'],
                'where': ["eqlponstr-col_cnpj_raiz-12345678-8-0-1-8"],
                'theme': 'rfbsocios'
            }
        )

class RfbParticipacaoSocietariaGetOptionsEmpresaTest(unittest.TestCase):
    ''' Class that tests translation of options from general to
        datasource-oriented ones '''
    def test_options_empresa_translation(self):
        ''' Tests if the options are correctly built according to given args '''
        self.assertEqual(
            RfbParticipacaoSocietaria().get_options_empresa(
                {'cnpj_raiz': '12345678'},
                {'cnpj_raiz': 'col_cnpj_raiz'},
                'rfbparticipacaosocietaria',
                None
            ),
            {
                'categorias': ['\'1\'-pos'],
                'agregacao': ['count'],
                'where': ["eqlponstr-col_cnpj_raiz-12345678-14-0-1-8", "and", "ne-nu_cnpj_cpf_socio-0", "and", "eq-id_tp_socio-1"],
                'theme': 'rfbparticipacaosocietaria'
            }
        )
