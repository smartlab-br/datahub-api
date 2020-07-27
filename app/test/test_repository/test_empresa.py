'''Main tests in API'''
import unittest
import pandas as pd
from repository.empresa.empresa import EmpresaRepository

class EmpresaRepositorySplitDataframePerspectiveTest(unittest.TestCase):
    ''' Tests dataset splitting by perspectives '''
    SOURCE_DATA = [
        {"cnpj": '12345678000101', 'origem_busca': 'Empregador'},
        {"cnpj": '12345678000202', 'origem_busca': 'Tomador'},
        {"cnpj": '12345678000303', 'origem_busca': 'Empregador Concessão'},
        {"cnpj": '12345678000404', 'origem_busca': 'Empregador AEPS'}
    ]
    EXPECTED_RESULT = {
        'catweb_empregador': [{'cnpj': '12345678000101', 'origem_busca': 'Empregador'}],
        'catweb_tomador': [{'cnpj': '12345678000202', 'origem_busca': 'Tomador'}],
        'catweb_concessao': [{'cnpj': '12345678000303', 'origem_busca': 'Empregador Concessão'}],
        'catweb_aeps': [{'cnpj': '12345678000404', 'origem_busca': 'Empregador AEPS'}]
    }
    def test_splitting_no_options(self):
        ''' Tests if an empty dictionary is returned when no data is sent '''
        self.assertEqual(
            EmpresaRepository().split_dataframe_by_perspective(None, None), {}
        )

    def test_splitting_no_data(self):
        ''' Tests if an empty dictionary is returned when no data is sent '''
        self.assertEqual(
            EmpresaRepository().split_dataframe_by_perspective(None, {}), {}
        )

    def test_splitting_emptys_data(self):
        ''' Tests if an empty dictionary is returned when empty data is sent '''
        self.assertEqual(
            EmpresaRepository().split_dataframe_by_perspective({}, {}), {}
        )

    def test_splitting_data_no_perspective(self):
        ''' Tests if an empty dictionary is returned when no data is sent '''
        self.assertEqual(
            EmpresaRepository().split_dataframe_by_perspective(
                {"rfb": pd.DataFrame([{"cnpj_raiz": '12345678'}])}, {}
            ),
            {}
        )

    def test_splitting(self):
        ''' Tests if data is split correctly '''
        self.maxDiff = None
        self.assertEqual(
            EmpresaRepository().split_dataframe_by_perspective(
                {"catweb": pd.DataFrame(self.SOURCE_DATA)}, {}
            ),
            self.EXPECTED_RESULT
        )

    def test_splitting_single_perspective(self):
        ''' Tests if data is split correctly when a perspective is given '''
        self.assertEqual(
            EmpresaRepository().split_dataframe_by_perspective(
                {"catweb": pd.DataFrame(self.SOURCE_DATA)}, {'perspective': 'empregador'}
            ),
            {"catweb_empregador": self.EXPECTED_RESULT.get('catweb_empregador')}
        )

    def test_splitting_mixed(self):
        ''' Tests if data is split correctly when data contains both a simple
            dataset and a splittable one '''
        self.assertEqual(
            EmpresaRepository().split_dataframe_by_perspective({
                "rfb": pd.DataFrame([{"cnpj_raiz": '12345678'}]),
                "catweb": pd.DataFrame(self.SOURCE_DATA)
            }, {}),
            self.EXPECTED_RESULT
        )
