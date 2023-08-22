'''Main tests in API'''
# import unittest
# from model.source.embarcacoes import Embarcacoes

# class EmbarcacoesGetOptionsEmpresaTest(unittest.TestCase):
#     ''' Class that tests translation of options from general to
#         datasource-oriented ones '''
#     def test_translation(self):
#         ''' Tests if the options are correctly built according to given args '''
#         self.assertEqual(
#             Embarcacoes().get_options_empresa(
#                 {'cnpj_raiz': '12345678'},
#                 {'cnpj_raiz': 'col_cnpj'},
#                 'embarcacoes',
#                 None
#             ),
#             {
#                 'categorias': ['col_cnpj'],
#                 'agregacao': ['count'],
#                 'where': ["eq-col_cnpj-12345678"],
#                 'theme': 'embarcacoes'
#             }
#         )
