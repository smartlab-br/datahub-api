'''Main tests in API'''
import unittest
from test.stubs.constants import COMMON_OPTIONS
from test.stubs.repository import StubFindModelRepository, StubFindModelCutRepository
from model.base import BaseModel

class StubFindModel(BaseModel):
    ''' Classe de STUB da abstração de models '''
    METADATA = {"fonte": 'Instituto STUB'}
    def get_repo(self):
        ''' Método abstrato para carregamento do repositório '''
        return StubFindModelRepository()

class StubFindModelCut(BaseModel):
    ''' Classe de STUB da abstração de models '''
    METADATA = {"fonte": 'Instituto STUB'}
    def get_repo(self):
        ''' Método abstrato para carregamento do repositório '''
        return StubFindModelCutRepository()

class BaseModelFindDatasetTest(unittest.TestCase):
    ''' Classe que testa a obtenção de dados de acordo com os parâmetros
        dados. '''
    def test_no_pivot(self):
        ''' Verifica se retorna o dataset apenas com o wrapping '''
        model = StubFindModel()

        self.assertEqual(
            model.find_dataset(
                {
                    **{
                        "categorias": [
                            'nm_indicador', 'nu_competencia', 'vl_indicador', 'lat_mun', 'long_mun'
                        ],
                        "pivot": None
                    },
                    **COMMON_OPTIONS
                }
            ),
            {
                "metadata": {"fonte": "Instituto STUB"},
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
            }
        )

    def test_no_wrap(self):
        ''' Verifica se retorna o dataset sem o wrapping '''
        model = StubFindModel()
        options = {
            **{
                "categorias": [
                    'nm_indicador', 'nu_competencia', 'vl_indicador', 'lat_mun', 'long_mun'
                ],
                "pivot": None,
                "no_wrap": True
            }, **COMMON_OPTIONS
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
        self.assertEqual(
            model.find_joined_dataset(
                {
                    "categorias": [
                        'nm_indicador', 'nu_competencia', 'vl_indicador',
                        'lat_mun', 'long_mun'
                    ],
                    "valor": ['vl_indicador'],
                    "agregacao": ['sum'],
                    "ordenacao": ['-nm_indicador'],
                    "where": ['eq-nu_competencia-2010'],
                    "joined": 'municipio',
                    "pivot": None
                }
            ),
            {
                "metadata": {"fonte": "Instituto STUB"},
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
            }
        )

class BaseModelFindAndOperateTest(unittest.TestCase):
    ''' Tests the behaviours linked to acting on data after retrieval '''
    def test_no_options(self):
        ''' Verifica se retorna o dataset apenas com o wrapping '''
        model = StubFindModelCut()
        self.assertRaises(
            AttributeError,
            model.find_and_operate,
            'cut',
            None
        )
