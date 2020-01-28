'''Main tests in API'''
import unittest
from test.test_model.test_setup_stubs import StubFindModel

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
