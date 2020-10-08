'''Main tests in API'''
import unittest
from test.stubs.constants import COMMON_OPTIONS
from test.stubs.repository import StubFindModelAgrRepository
from model.base import BaseModel

class StubFindModelAgr(BaseModel):
    ''' Classe de STUB da abstração de models '''
    METADATA = {"fonte": 'Instituto STUB'}
    def get_repo(self):
        ''' Método abstrato para carregamento do repositório '''
        return StubFindModelAgrRepository()

class BaseModelFindPivotedDatasetTest(unittest.TestCase):
    ''' Classe que testa a obtenção de dados com pivoting. '''
    def test_pivot(self):
        ''' Verifica se retorna o dataset pivotado e com o wrapping '''
        model = StubFindModelAgr()
        self.assertEqual(
            model.find_dataset({
                **{
                    "categorias": ['nm_indicador'],
                    "pivot": "nu_competencia",
                    "calcs": None
                },
                **COMMON_OPTIONS
            }),
            {
                "metadata": {"fonte": "Instituto STUB"},
                "dataset": [{
                    "nm_indicador": "Ficticio",
                    2047: 0.5,
                    2099: 1.0
                }]
            }
        )
