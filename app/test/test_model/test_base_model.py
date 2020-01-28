'''Main tests in API'''
import unittest
import numpy as np
import pandas as pd
from model.base import BaseModel

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
SAMPLE_DATAFRAME_REAL = pd.DataFrame.from_dict(
    {
        'col_1': ['d', 'b', 'a', 'c'],
        'col_2': [3000.3, 2000.2, 1000.1, 0.0],
        'col_3': [3000.3, 2000.2, 1000.1, 0.0],
        'col_4': [3000.3, 2000.2, 1000.1, 0.0],
        'col_5': [3000.3, 2000.2, 1000.1, None]
    }
)

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
    def test_del_keywords(self):
        ''' Tests removal of keywords from configuration after usage '''
        self.assertEqual(
            BaseModel.del_keywords({"as_is": True, "keep_template": False, "test": "test"}),
            {"test": "test"}
        )

    def test_get_terms(self):
        ''' Test if custom terms form a dictionary correctly '''
        self.assertEqual(
            BaseModel.get_terms('first-test,second-term'),
            {"term_first": {"value" : "test"}, "term_second": {"value": "term"}}
        )

    def test_get_coefficients(self):
        ''' Test if custom coefficients form a dictionary correctly '''
        self.assertEqual(
            BaseModel.get_coefficients('first-1.2-test,second-3-term'),
            {
                "coef_first": {"value": 1.2, "label": "test"},
                "coef_second": {"value": 3, "label": "term"}
            }
        )

    def test_apply_coefficients(self):
        ''' Test if custom coefficients are applied correctly to a dataset '''
        self.assertEqual(
            BaseModel.apply_coefficient(
                'col_2-2-test,col_3-3-term',
                {"dataset": SAMPLE_DATAFRAME.copy()}
            )["dataset"].to_dict(),
            {
                'col_1': {0: 'd', 1: 'b', 2: 'a', 3: 'c'},
                'col_2': {0: 6.0, 1: 4.0, 2: 2.0, 3: 0.0},
                'col_3': {0: 9.0, 1: 6.0, 2: 3.0, 3: 0.0}
            }
        )

    def test_run_formatters(self):
        ''' Test if formatters run correctly given the dataset and format options '''
        self.assertEqual(
            BaseModel.run_formatters(
                [
                    {
                        "prop": "col_2",
                        "named_prop": "col_2",
                        "format": 'real',
                        "precision": 1,
                    },
                    {
                        "prop": "col_3",
                        "named_prop": "col_3",
                        "format": 'inteiro',
                        "multiplier": 2
                    },
                    {
                        "prop": "col_4",
                        "named_prop": "col_4",
                        "format": 'real',
                        "collapse": {"format": "inteiro"}
                    },
                    {
                        "prop": "col_5",
                        "named_prop": "col_5",
                        "format": 'real',
                        "default": "N/A"
                    }
                ],
                {"dataset": SAMPLE_DATAFRAME_REAL.copy()}
            )['dataset'].to_dict(),
            ({
                'col_1': {0: 'd', 1: 'b', 2: 'a', 3: 'c'},
                'col_2': {0: "3.000,3", 1: "2.000,2", 2: "1.000,1", 3: "0"},
                'col_3': {0: "6.001", 1: "4.000", 2: "2.000", 3: "0"},
                'col_4': {
                    0: "3<span>mil</span>", 1: "2<span>mil</span>", 2: "1<span>mil</span>", 3: "0"
                },
                'col_5': {0: "3.000", 1: "2.000", 2: "1.000", 3: "N/A"}
            })
        )

    def test_get_formatted_value_from_object(self):
        ''' Test if object attribute is correctly formatted. '''
        self.assertEqual(
            BaseModel.get_formatted_value(
                {"base_object": "obj1", "named_prop": "field1", "format": "monetario"},
                {"obj1": {"field1": 1.0}}
            ),
            "<span>R$</span>1"
        )

class BaseModelTemplateSortingTest(unittest.TestCase):
    ''' Test sorting in template processing '''
    def test_resort_dataset_all_asc(self):
        ''' Test if dataset is ordered ascending if all args are ascending '''
        self.assertEqual(
            BaseModel.resort_dataset(
                SAMPLE_DATAFRAME,
                ["col_1", "col_2"]
            ).to_dict('split')['data'],
            [['a', 1, 1], ['b', 2, 2], ['c', 0, 0], ['d', 3, 3]]
        )

    def test_resort_dataset_mixed(self):
        ''' Test if dataset is ordered ascending if any arg is ascending '''
        self.assertEqual(
            BaseModel.resort_dataset(
                SAMPLE_DATAFRAME,
                ["-col_1", "-col_2", "col_3"]
            ).to_dict('split')['data'],
            [['a', 1, 1], ['b', 2, 2], ['c', 0, 0], ['d', 3, 3]]
        )

    def test_resort_dataset_desc(self):
        ''' Test if dataset is ordered descending if all args are descending '''
        self.assertEqual(
            BaseModel.resort_dataset(
                SAMPLE_DATAFRAME,
                ["-col_1", "-col_2", "-col_3"]
            ).to_dict('split')['data'],
            [['d', 3, 3], ['c', 0, 0], ['b', 2, 2], ['a', 1, 1]]
        )

    def test_resort_dataset_no_rule(self):
        ''' Test if dataset resturns as is if no order rule is sent '''
        self.assertEqual(
            BaseModel.resort_dataset(
                SAMPLE_DATAFRAME,
                ["col_1", "col_2"]
            ).to_dict('split')['data'],
            [['a', 1, 1], ['b', 2, 2], ['c', 0, 0], ['d', 3, 3]]
        )

class BaseModelTemplateFilteringTest(unittest.TestCase):
    ''' Test filters in template processing '''
    def test_filter_dataset_nofilter(self):
        ''' Test if dataset returns when no filter is actually sent '''
        self.assertEqual(
            BaseModel.filter_pandas_dataset(SAMPLE_DATAFRAME, None).to_dict(),
            {
                'col_1': {0: 'd', 1: 'b', 2: 'a', 3: 'c'},
                'col_2': {0: 3, 1: 2, 2: 1, 3: 0},
                'col_3': {0: 3, 1: 2, 2: 1, 3: 0}
            }
        )

    def test_filter_dataset_eq(self):
        ''' Test if dataset is filtered by EQ clause '''
        self.assertEqual(
            BaseModel.filter_pandas_dataset(
                SAMPLE_DATAFRAME,
                [['post', 'eq', 'col_2', '3']]
            ).to_dict(),
            {
                'col_1': {0: 'd'},
                'col_2': {0: 3},
                'col_3': {0: 3}
            }
        )

    def test_filter_dataset_nn(self):
        ''' Test if dataset is filtered by NN clause '''
        self.assertEqual(
            BaseModel.filter_pandas_dataset(
                SAMPLE_DATAFRAME_NA,
                [['post', 'nn', 'col_2']]
            ).to_dict(),
            {
                'col_1': {0: 'd', 1: 'b', 2: 'a'},
                'col_2': {0: 3, 1: 2, 2: 1},
                'col_3': {0: 3, 1: 2, 2: 1}
            }
        )

    def test_filter_dataset_in(self):
        ''' Test if dataset is filtered by IN clause '''
        self.assertEqual(
            BaseModel.filter_pandas_dataset(
                SAMPLE_DATAFRAME,
                [['post', 'in', 'col_2', '3', '2']]
            ).to_dict(),
            {
                'col_1': {0: 'd', 1: 'b'},
                'col_2': {0: 3, 1: 2},
                'col_3': {0: 3, 1: 2}
            }
        )

    def test_filter_dataset_mixed(self):
        ''' Test if dataset is filtered by multiple clauses '''
        self.assertEqual(
            BaseModel.filter_pandas_dataset(
                SAMPLE_DATAFRAME_NA,
                [['post', 'in', 'col_3', '3', '1'], ['post', 'in', 'col_2', '3', '2']]
            ).to_dict(),
            {
                'col_1': {0: 'd'},
                'col_2': {0: 3},
                'col_3': {0: 3}
            }
        )

    def test_reform_filters_no_filter(self):
        ''' Test if None is returned if no filter is sent to the method '''
        self.assertEqual(
            BaseModel.reform_filters_for_pandas(None),
            (None, None)
        )

    def test_reform_filters_full(self):
        ''' Test if filters are classified correctly as pre and post '''
        self.assertEqual(
            BaseModel.reform_filters_for_pandas(
                ['post-eq-a-1', 'and', 'in-b-2-3', 'and', 'post-nn-c', 'or', 'eq-d-4']
            ),
            (
                ['in-b-2-3', 'and', 'eq-d-4'],
                [['post', 'eq', 'a', '1'], 'and', ['post', 'nn', 'c']]
            )
        )

class BaseModelTemplateCollectionsTest(unittest.TestCase):
    ''' Test collections manipulation in template processing '''
    def test_get_collection_from_type_from_id(self):
        ''' Test if the method returns the item with the passed numeric id '''
        self.assertEqual(
            BaseModel.get_collection_from_type(
                SAMPLE_DATAFRAME.copy(),
                "from_id",
                "col_2",
                2
            ).to_dict(),
            {"col_1": "b", "col_2": 2, "col_3": 2}
        )

    def test_get_collection_from_type_from_invalid_id(self):
        ''' Test if the method returns the item with the passed string id '''
        self.assertRaises(
            ValueError,
            BaseModel.get_collection_from_type,
            SAMPLE_DATAFRAME.copy(),
            "from_id",
            "col_1",
            'a'
        )

    def test_get_collection_from_type_min(self):
        ''' Test if the method returns the item with minimum value in colum '''
        self.assertEqual(
            BaseModel.get_collection_from_type(
                SAMPLE_DATAFRAME.copy(),
                "min",
                "col_2"
            ).to_dict(),
            {"col_1": "c", "col_2": 0, "col_3": 0}
        )

    def test_get_collection_from_type_max(self):
        ''' Test if the method returns the item with maximum value in colum '''
        self.assertEqual(
            BaseModel.get_collection_from_type(
                SAMPLE_DATAFRAME.copy(),
                "max",
                "col_2"
            ).to_dict(),
            {"col_1": "d", "col_2": 3, "col_3": 3}
        )

    def test_get_collection_from_type_first_occurence(self):
        ''' Test if the method returns the first item '''
        self.assertEqual(
            BaseModel.get_collection_from_type(
                SAMPLE_DATAFRAME.copy(),
                "first_occurence"
            ).to_dict(),
            {"index": 0, "col_1": "d", "col_2": 3, "col_3": 3}
        )

    def test_get_collection_from_missing_type(self):
        ''' Test if the method returns None if no type is passed '''
        self.assertEqual(
            BaseModel.get_collection_from_type(
                SAMPLE_DATAFRAME.copy(),
                None
            ),
            None
        )

    def test_get_collection_from_invalid_type(self):
        ''' Test if the method returns None if an invalid type is passed '''
        self.assertEqual(
            BaseModel.get_collection_from_type(
                SAMPLE_DATAFRAME.copy(),
                'invalid'
            ),
            None
        )

    def test_build_derivatives(self):
        ''' Test if derivate object is added to the collection '''
        options = {'cd_analysis_unit': 2}
        rules = {
            "instances": [{"name": "inst_1", 'type': 'max', 'named_prop': 'col_2'}]
        }
        sources = {"dataset": SAMPLE_DATAFRAME.copy()}
        (der_data, der_anynodata) = BaseModel.build_derivatives(
            rules,
            options,
            sources,
            {}
        )
        self.assertEqual(
            der_data["inst_1"].to_dict(),
            {"col_1": "d", "col_2": 3, "col_3": 3}
        )
        self.assertEqual(der_anynodata, False)

    def test_build_derivatives_nodata(self):
        ''' Test the derivate objects is added with no_data flag '''
        options = {'cd_analysis_unit': 99}
        rules = {
            "instances": [{"name": "inst_1", 'type': 'from_id', 'named_prop': 'col_2'}]
        }
        sources = {"dataset": SAMPLE_DATAFRAME.copy()}
        (der_data, der_anynodata) = BaseModel.build_derivatives(
            rules,
            options,
            sources,
            {}
        )
        self.assertEqual(
            der_data["inst_1"],
            None
        )
        self.assertEqual(der_anynodata, True)
