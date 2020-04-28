'''Main tests in API'''
import unittest
from test.stubs.constants import SAMPLE_DATAFRAME, SAMPLE_DATAFRAME_REAL
from service.template_helper import TemplateHelper

class TemplateHelperTest(unittest.TestCase):
    ''' Test behaviours linked to first-tier template interpolation '''
    def test_del_keywords(self):
        ''' Tests removal of keywords from configuration after usage '''
        self.assertEqual(
            TemplateHelper.del_keywords({"as_is": True, "keep_template": False, "test": "test"}),
            {"test": "test"}
        )

    def test_get_terms(self):
        ''' Test if custom terms form a dictionary correctly '''
        self.assertEqual(
            TemplateHelper.get_terms('first-test,second-term'),
            {"term_first": {"value" : "test"}, "term_second": {"value": "term"}}
        )

    def test_get_coefficients(self):
        ''' Test if custom coefficients form a dictionary correctly '''
        self.assertEqual(
            TemplateHelper.get_coefficients('first-1.2-test,second-3-term'),
            {
                "coef_first": {"value": 1.2, "label": "test"},
                "coef_second": {"value": 3, "label": "term"}
            }
        )

    def test_apply_coefficients(self):
        ''' Test if custom coefficients are applied correctly to a dataset '''
        self.assertEqual(
            TemplateHelper.apply_coefficient(
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
            TemplateHelper.run_formatters(
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
            TemplateHelper.get_formatted_value(
                {"base_object": "obj1", "named_prop": "field1", "format": "monetario"},
                {"obj1": {"field1": 1.0}}
            ),
            "<span>R$</span>1"
        )


class TemplateHelperRunNamedFunctionTest(unittest.TestCase):
    ''' Test functions calls by reflection '''
    def test_run_slice_function(self):
        ''' Test slicing a dataframe object '''
        self.assertEqual(
            TemplateHelper.run_named_function(
                {
                    'function': 'slice',
                    'args': [{"fixed": 0}, {"fixed": 2}]
                },
                list(range(10))
            ),
            [0, 1]
        )

    def test_run_slice_function_ignore_non_fixed_args(self):
        ''' Test if non-fixed args are ignored correctly '''
        self.assertEqual(
            TemplateHelper.run_named_function(
                {
                    'function': 'slice',
                    'args': [{"fixed": 0}, {"prop": "vals"}, {"fixed": 2}]
                },
                list(range(10))
            ),
            [0, 1]
        )

    def test_run_slice_function_on_object(self):
        ''' Test slicing a dataframe object '''
        # Defining a custom class for instantiation
        #pylint: disable=R0903
        class CustomClass():
            ''' Creating a class for running its function '''
            vals = list(range(10))
            def fake_slice(self, limit):
                ''' Method to call by reflection '''
                return self.vals[limit:]
        # Running test
        self.assertEqual(
            TemplateHelper.run_named_function(
                {
                    'function': 'fake_slice',
                    'args': [{"fixed": 5}]
                },
                CustomClass()
            ),
            [5, 6, 7, 8, 9]
        )
