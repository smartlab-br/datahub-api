''' Testes do formatador '''
import unittest
from service.qry_options_builder import QueryOptionsBuilder

class OptionsBuilderTest(unittest.TestCase):
    ''' Classe que testa a construção de options a partir dos parâmetros do request '''
    def test_no_categories(self):
        ''' Verifica se o parâmetro obrigatório de categorias está presente '''
        self.assertRaises(ValueError, QueryOptionsBuilder.build_options, {})

    def test_full_args(self):
        ''' Verifica se os parâmetros são criados corretamente '''
        r_args = {
            "categorias": 'a,b',
            "valor": 'c,d',
            "agregacao": 'e,f',
            "ordenacao": 'g,h',
            "filtros": 'eq-o-comma\,separated,and,eq-p-q',
            "pivot": 'i,j',
            "limit": '10',
            "offset": '11',
            "calcs": 'k,l',
            "partition": 'm,n',
            "theme": 't'
        }

        opts = QueryOptionsBuilder.build_options(r_args)
        
        self.assertEqual(
            opts,
            {
                "categorias": ['a','b'],
                "valor": ['c','d'],
                "agregacao": ['e','f'],
                "ordenacao": ['g','h'],
                "where": ['eq-o-comma,separated','and','eq-p-q'],
                "pivot": ['i','j'],
                "limit": '10',
                "offset": '11',
                "calcs": ['k','l'],
                "partition": ['m','n'],
                "theme": 't'
            }
        )

    def test_main_theme(self):
        ''' Verifica se os parâmetros são criados corretamente '''
        r_args = {
            "categorias": 'a,b',
            "valor": 'c,d',
            "agregacao": 'e,f',
            "ordenacao": 'g,h',
            "where": 'eq-o-comma\,separated,and,eq-p-q',
            "pivot": 'i,j',
            "limit": '10',
            "offset": '11',
            "calcs": 'k,l',
            "partition": 'm,n'
        }

        opts = QueryOptionsBuilder.build_options(r_args)
        
        self.assertEqual(opts.get('theme'), None)
