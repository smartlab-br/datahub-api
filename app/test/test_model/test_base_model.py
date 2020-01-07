'''Main tests in API'''
import unittest
import numpy as np
import pandas as pd
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

class BaseModelTemplateTest(unittest.TestCase):
    ''' Test behaviours linked to first-tier template interpolation '''
    SAMPLE_DATAFRAME = pd.DataFrame.from_dict(
        {
            'col_1': ['d', 'b', 'a', 'c'],
            'col_2': [3, 2, 1, 0],
            'col_3': [3, 2, 1, 0]
        }
    )
    SAMPLE_DATAFRAME_NA = pd.DataFrame.from_dict(
        {
            'col_1': ['d', 'b', 'a', 'c'],
            'col_2': [3, 2, 1, None],
            'col_3': [3, 2, 1, None]
        }
    )

    def test_del_keywords(self):
        ''' Tests removal of keywords from configuration after usage '''
        self.assertEqual(
            BaseModel.del_keywords({ "as_is": True, "keep_template": False, "test": "test" }),
            { "test": "test" }
        )
    
    def test_get_terms(self):
        ''' Test if custom terms form a dictionary correctly '''
        self.assertEqual(
            BaseModel.get_terms('first-test,second-term'),
            { "term_first": { "value" : "test" }, "term_second": { "value": "term" } }
        )   

    def test_get_coefficients(self):
        ''' Test if custom coefficients form a dictionary correctly '''
        self.assertEqual(
            BaseModel.get_coefficients('first-1.2-test,second-3-term'),
            { 
                "coef_first": { "value": 1.2, "label": "test" },
                "coef_second": { "value": 3, "label": "term" }
            }
        )
    
    def test_apply_coefficients(self):
        ''' Test if custom coefficients are applied correctly to a dataset '''
        self.assertEqual(
            BaseModel.apply_coefficient(
                'col_2-2-test,col_3-3-term',
                { "dataset": self.SAMPLE_DATAFRAME.copy() }
            )["dataset"].to_dict(),
            { 
                'col_1': { 0: 'd', 1: 'b', 2: 'a', 3: 'c' },
                'col_2': { 0: 6.0, 1: 4.0, 2: 2.0, 3: 0.0 },
                'col_3': { 0: 9.0, 1: 6.0, 2: 3.0, 3: 0.0 }
            }
        )
    
    def test_resort_dataset_all_asc(self):
        ''' Test if dataset is ordered ascending if all args are ascending '''
        self.assertEqual(
            BaseModel.resort_dataset(
                self.SAMPLE_DATAFRAME,
                ["col_1", "col_2"]
            ).to_dict('split')['data'],
            [['a', 1, 1], ['b', 2, 2], ['c', 0, 0], ['d', 3, 3]]
        ) 

    def test_resort_dataset_mixed(self):
        ''' Test if dataset is ordered ascending if any arg is ascending '''
        self.assertEqual(
            BaseModel.resort_dataset(
                self.SAMPLE_DATAFRAME,
                ["-col_1", "-col_2", "col_3"]
            ).to_dict('split')['data'],
            [['a', 1, 1], ['b', 2, 2], ['c', 0, 0], ['d', 3, 3]]
        ) 

    def test_resort_dataset_desc(self):
        ''' Test if dataset is ordered descending if all args are descending '''
        self.assertEqual(
            BaseModel.resort_dataset(
                self.SAMPLE_DATAFRAME,
                ["-col_1", "-col_2", "-col_3"]
            ).to_dict('split')['data'],
            [['d', 3, 3], ['c', 0, 0], ['b', 2, 2], ['a', 1, 1]]
        ) 
    
    def test_filter_dataset_nofilter(self):
        ''' Test if dataset returns when no filter is actually sent '''
        self.assertEqual(
            BaseModel.filter_pandas_dataset(self.SAMPLE_DATAFRAME, None).to_dict(),
            { 
                'col_1': { 0: 'd', 1: 'b', 2: 'a', 3: 'c' },
                'col_2': { 0: 3, 1: 2, 2: 1, 3: 0 },
                'col_3': { 0: 3, 1: 2, 2: 1, 3: 0 }
            }
        )
    
    def test_filter_dataset_eq(self):
        ''' Test if dataset is filtered by EQ clause '''
        self.assertEqual(
            BaseModel.filter_pandas_dataset(
                self.SAMPLE_DATAFRAME,
                [['post', 'eq', 'col_2', '3']]
            ).to_dict(),
            { 
                'col_1': { 0: 'd' },
                'col_2': { 0: 3 },
                'col_3': { 0: 3 }
            }
        ) 

    def test_filter_dataset_nn(self):
        ''' Test if dataset is filtered by NN clause '''
        self.assertEqual(
            BaseModel.filter_pandas_dataset(
                self.SAMPLE_DATAFRAME_NA,
                [['post', 'nn', 'col_2']]
            ).to_dict(),
            { 
                'col_1': { 0: 'd', 1: 'b', 2: 'a' },
                'col_2': { 0: 3, 1: 2, 2: 1 },
                'col_3': { 0: 3, 1: 2, 2: 1 }
            }
        ) 
    
    def test_filter_dataset_in(self):
        ''' Test if dataset is filtered by IN clause '''
        self.assertEqual(
            BaseModel.filter_pandas_dataset(
                self.SAMPLE_DATAFRAME,
                [['post', 'in', 'col_2', '3', '2']]
            ).to_dict(),
            { 
                'col_1': { 0: 'd', 1: 'b' },
                'col_2': { 0: 3, 1: 2 },
                'col_3': { 0: 3, 1: 2 }
            }
        ) 

    def test_filter_dataset_mixed(self):
        ''' Test if dataset is filtered by multiple clauses '''
        self.assertEqual(
            BaseModel.filter_pandas_dataset(
                self.SAMPLE_DATAFRAME_NA,
                [['post', 'in', 'col_3', '3', '1'], ['post', 'in', 'col_2', '3', '2']]
            ).to_dict(),
            { 
                'col_1': { 0: 'd' },
                'col_2': { 0: 3 },
                'col_3': { 0: 3 }
            }
        ) 