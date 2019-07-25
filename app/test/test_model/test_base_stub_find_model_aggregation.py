'''Main tests in API'''
import unittest
import pandas as pd
from model.base import BaseModel
from repository.base import HadoopRepository

class StubFindModel(BaseModel):
    ''' Classe de STUB da abstração de models '''
    METADATA = {
        "fonte": 'Instituto STUB'
    }
    def get_repo(self):
        ''' Método abstrato para carregamento do repositório '''
        return StubFindModelRepository()

class StubFindModelRepository(HadoopRepository):
    ''' Fake repo to test instance methods '''
    TABLE_NAMES = {
        'MAIN': 'indicadores',
        'municipio': 'municipio'
    }
    JOIN_SUFFIXES = {
        'municipio': '_mun'
    }
    ON_JOIN = {
        'municipio': 'cd_mun_ibge = cd_municipio_ibge_dv'
    }
    NAMED_QUERIES = {
        'QRY_FIND_DATASET': 'SELECT {} FROM {} {} {} {}',
        'QRY_FIND_JOINED_DATASET': 'SELECT {} FROM {} LEFT JOIN {} ON {} {} {} {}'
    }
    def load_and_prepare(self):
        self.dao = 'Instanciei o DAO'

    def find_joined_dataset(self, options=None):
        return self.find_dataset(options)

    def find_dataset(self, options=None):
        ''' Retorno estático para execução dos testes '''
        from io import StringIO

        str_dataset = StringIO(
            """nm_indicador;nu_competencia;agr_sum_vl_indicador
                Ficticio;2099;1
                Ficticio;2047;0.5
                """
        )
        dataset = pd.read_csv(str_dataset, sep=";")
        return dataset

class BaseModelFindPivotedDatasetTest(unittest.TestCase):
    ''' Classe que testa a obtenção de dados com pivoting. '''
    def test_pivot(self):
        ''' Verifica se retorna o dataset pivotado e com o wrapping '''
        model = StubFindModel()

        options = {
            "categorias": ['nm_indicador'],
            "valor": ['vl_indicador'],
            "agregacao": ['sum'],
            "ordenacao": ['-nm_indicador'],
            "where": ['eq-nu_competencia-2010'],
            "joined": None,
            "pivot": "nu_competencia",
            "calcs": None
        }
        str_result = model.find_dataset(options)
        result = "".join(str_result.split())

        str_expected = """{
            "metadata": {
                "fonte": "Instituto STUB"
            },
            "dataset": [
                {
                    "nm_indicador": "Ficticio",
                    "2047":0.5,
                    "2099":1.0
                }
            ]
        }"""
        expected = "".join(str_expected.split())

        self.assertEqual(result, expected)
