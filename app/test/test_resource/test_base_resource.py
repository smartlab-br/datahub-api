'''Main tests in API'''
import unittest
from resources.base import BaseResource

class BaseResourceBuildOptionsTest(unittest.TestCase):
    ''' Classe que testa a validação do field array '''
    def test_block_null_cats(self):
        ''' Verifica se é rejeitada entrada nula de categorias '''
        qry_params = {
            "categorias": None
        }
        self.assertRaises(
            ValueError,
            BaseResource.build_options,
            qry_params
        )

    def test_block_empty_cats(self):
        ''' Verifica se é rejeitada entrada nula de categorias '''
        qry_params = {
            "categorias": ''
        }
        self.assertRaises(
            ValueError,
            BaseResource.build_options,
            qry_params
        )

    def test_allow(self):
        ''' Verifica a correta construção de parâmetros '''
        qry_params = {
            "categorias":
                'cd_municipio,nm_indicador,vl_indicador,nu_competencia',
            "valor": 'vl_indicador',
            "agregacao": 'sum',
            "ordenacao": '-vl_indicador',
            "filtros": 'eq-nu_competencia-2010',
            "pivot": 'nm_indicador',
            "limit": None,
            "offset": None,
            "calcs": None,
            "partition": None
        }
        expected = {
            "categorias": [
                'cd_municipio', 'nm_indicador', 'vl_indicador',
                'nu_competencia'
            ],
            "valor": ['vl_indicador'],
            "agregacao": ['sum'],
            "ordenacao": ['-vl_indicador'],
            "where": ['eq-nu_competencia-2010'],
            "pivot": ['nm_indicador'],
            "limit": None,
            "offset": None,
            "calcs": None,
            "partition": None
        }
        built = BaseResource.build_options(qry_params)
        self.assertEqual(built, expected)

    def test_allow_comma(self):
        ''' Verifica a correta construção de parâmetros quando há uma vírgula no filtro'''
        qry_params = {
            "categorias":
                'cd_municipio,nm_indicador,vl_indicador,nu_competencia',
            "valor": 'vl_indicador',
            "agregacao": 'sum',
            "ordenacao": '-vl_indicador',
            "filtros": 'eq-ds_indicador-Acidentes\, B91,and,eq-nu_competencia-2010',
            "pivot": 'nm_indicador',
            "limit": None,
            "offset": None,
            "calcs": None,
            "partition": None
        }
        expected = {
            "categorias": [
                'cd_municipio', 'nm_indicador', 'vl_indicador',
                'nu_competencia'
            ],
            "valor": ['vl_indicador'],
            "agregacao": ['sum'],
            "ordenacao": ['-vl_indicador'],
            "where": ['eq-ds_indicador-Acidentes, B91', 'and', 'eq-nu_competencia-2010'],
            "pivot": ['nm_indicador'],
            "limit": None,
            "offset": None,
            "calcs": None,
            "partition": None
        }
        built = BaseResource.build_options(qry_params)
        self.assertEqual(built, expected)

def test_allow_hyphen_and_comma(self):
        ''' Verifica a correta construção de parâmetros quando há uma vírgula ou hífen no filtro'''
        qry_params = {
            "categorias":
                'cd_municipio,nm_indicador,vl_indicador,nu_competencia',
            "valor": 'vl_indicador',
            "agregacao": 'sum',
            "ordenacao": '-vl_indicador',
            "filtros": 'eq-ds_indicador-Acidentes\, B91\-,and,eq-nu_competencia-2010',
            "pivot": 'nm_indicador',
            "limit": None,
            "offset": None,
            "calcs": None,
            "partition": None
        }
        expected = {
            "categorias": [
                'cd_municipio', 'nm_indicador', 'vl_indicador',
                'nu_competencia'
            ],
            "valor": ['vl_indicador'],
            "agregacao": ['sum'],
            "ordenacao": ['-vl_indicador'],
            "where": ['eq-ds_indicador-Acidentes, B91\-', 'and', 'eq-nu_competencia-2010'],
            "pivot": ['nm_indicador'],
            "limit": None,
            "offset": None,
            "calcs": None,
            "partition": None
        }
        built = BaseResource.build_options(qry_params)
        self.assertEqual(built, expected)