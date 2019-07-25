'''Main tests in API'''
import unittest
import numpy as np
from model.base import BaseModel

class BaseModelGetPandasAggregationTest(unittest.TestCase):
    ''' Classe que testa o mapeamento de agregações para funções do pandas '''
    def test_default_on_none(self):
        ''' Verifica se retorna np.mean se agregação nula '''
        self.assertEqual(BaseModel.aggr_to_np(None), np.mean)

    def test_default_on_empty(self):
        ''' Verifica se retorna np.mean se agragação vazia '''
        self.assertEqual(BaseModel.aggr_to_np(''), np.mean)

    def test_default_on_unmapped(self):
        ''' Verifica se retorna np.mean se agregação não prevista '''
        self.assertEqual(BaseModel.aggr_to_np('xpto'), np.mean)

    def test_sum(self):
        ''' Verifica se retorna np.sum '''
        self.assertEqual(BaseModel.aggr_to_np('sum'), np.sum)

    def test_sum_on_count(self):
        ''' Verifica se não retorna nada e a agregação for count '''
        self.assertEqual(BaseModel.aggr_to_np('count'), np.sum)

class BaseModelConvertAggregationToPandasTest(unittest.TestCase):
    ''' Classe que testa o mapeamento de coleção de agregações para funções
        do pandas '''
    def test_single_aggr(self):
        ''' Verifica se retorna np.mean se agregação nula '''
        model = BaseModel()
        aggrs = 'sum'
        self.assertEqual(model.convert_aggr_to_np(aggrs, None), np.sum)

    def test_multiple_aggr(self):
        ''' Verifica se retorna np.mean se agregação nula '''
        model = BaseModel()
        aggrs = ['sum', 'count', 'xpto', '']
        vals = ['vl_indicador', 'cd_municipio', 'nu_competencia',
                'another_field']
        expected = {
            'vl_indicador': np.sum,
            'cd_municipio': np.sum,
            'nu_competencia': np.mean,
            'another_field': np.mean
        }
        self.assertEqual(model.convert_aggr_to_np(aggrs, vals), expected)
