'''Main tests in API'''
import unittest
from io import StringIO
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
        ''' Overriding method outside test scope '''
        self.dao = 'Instanciei o DAO'

    def find_joined_dataset(self, options=None):
        ''' Overriding method outside test scope '''
        return self.find_dataset(options)

    def find_dataset(self, options=None):
        ''' Retorno estático para execução dos testes '''
        str_dataset = StringIO(
            """nm_indicador;nu_competencia;vl_indicador
                Ficticio;2099;1
                Ficticio;2047;0.5
                """
        )
        dataset = pd.read_csv(str_dataset, sep=";")
        return dataset

class BaseModelFindDatasetTest(unittest.TestCase):
    ''' Classe que testa a obtenção de dados de acordo com os parâmetros
        dados. '''
    def test_no_pivot(self):
        ''' Verifica se retorna o dataset apenas com o wrapping '''
        model = StubFindModel()

        options = {
            "categorias": ['nm_indicador', 'nu_competencia', 'vl_indicador', 'lat_mun', 'long_mun'],
            "valor": ['vl_indicador'],
            "agregacao": ['sum'],
            "ordenacao": ['-nm_indicador'],
            "where": ['eq-nu_competencia-2010'],
            "joined": None,
            "pivot": None
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
                    "nu_competencia": 2099,
                    "vl_indicador": 1.0
                },
                {
                    "nm_indicador": "Ficticio",
                    "nu_competencia": 2047,
                    "vl_indicador": 0.5
                }
            ]
        }"""
        expected = "".join(str_expected.split())

        self.assertEqual(result, expected)

    def test_no_wrap(self):
        ''' Verifica se retorna o dataset sem o wrapping '''
        model = StubFindModel()

        options = {
            "categorias": ['nm_indicador', 'nu_competencia', 'vl_indicador', 'lat_mun', 'long_mun'],
            "valor": ['vl_indicador'],
            "agregacao": ['sum'],
            "ordenacao": ['-nm_indicador'],
            "where": ['eq-nu_competencia-2010'],
            "joined": None,
            "pivot": None,
            "no_wrap": True
        }
        str_result = model.find_dataset(options).to_json(orient="records")
        result = "".join(str_result.split())

        str_expected = """[
                {
                    "nm_indicador": "Ficticio",
                    "nu_competencia": 2099,
                    "vl_indicador": 1.0
                },
                {
                    "nm_indicador": "Ficticio",
                    "nu_competencia": 2047,
                    "vl_indicador": 0.5
                }]"""
        expected = "".join(str_expected.split())

        self.assertEqual(result, expected)


class BaseModelFindJoinedDatasetTest(unittest.TestCase):
    ''' Classe que testa a obtenção de dados de acordo com os parâmetros
        dados. '''
    def test_no_pivot(self):
        ''' Verifica se retorna o dataset apenas com o wrapping '''
        model = StubFindModel()

        options = {
            "categorias": ['nm_indicador', 'nu_competencia', 'vl_indicador', 'lat_mun', 'long_mun'],
            "valor": ['vl_indicador'],
            "agregacao": ['sum'],
            "ordenacao": ['-nm_indicador'],
            "where": ['eq-nu_competencia-2010'],
            "joined": 'municipio',
            "pivot": None
        }
        str_result = model.find_joined_dataset(options)
        result = "".join(str_result.split())

        str_expected = """{
            "metadata": {
                "fonte": "Instituto STUB"
            },
            "dataset": [
                {
                    "nm_indicador": "Ficticio",
                    "nu_competencia": 2099,
                    "vl_indicador": 1.0
                },
                {
                    "nm_indicador": "Ficticio",
                    "nu_competencia": 2047,
                    "vl_indicador": 0.5
                }
            ]
        }"""
        expected = "".join(str_expected.split())

        self.assertEqual(result, expected)
