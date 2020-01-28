'''Main tests in API'''
import unittest
from io import StringIO
import pandas as pd
from model.base import BaseModel

class StubModel(BaseModel):
    ''' Classe de STUB da abstração de models '''
    METADATA = {
        "fonte": 'Instituto STUB'
    }
    def get_repo(self):
        ''' Método abstrato para carregamento do repositório '''
        return 'My repo'

class BaseModelFetchMetadataTest(unittest.TestCase):
    ''' Classe que testa a obtenção dos metadados definidos no model,
        para inserção no resultado das consultas. '''
    def test_fetch(self):
        ''' Verifica se retorna exatamente o atributo definido no model '''
        model = StubModel()
        expected = {"fonte": 'Instituto STUB'}
        self.assertEqual(model.fetch_metadata(), expected)

class BaseModelGetRepoTest(unittest.TestCase):
    ''' Classe que testa a obtenção de um repo, conforme definição do model '''
    def test_no_def(self):
        ''' Verifica se retorna np.mean se agregação nula '''
        model = BaseModel()
        self.assertRaises(
            NotImplementedError,
            model.get_repo
        )

    def test_valid_model(self):
        ''' Verifica se retorna np.mean se agregação nula '''
        model = StubModel()
        self.assertEqual(model.get_repo(), 'My repo')

class BaseModelWrapResultTest(unittest.TestCase):
    ''' Classe que verifica se os metadados são inseridos corretamente
        no objeto de retorno do dataset '''
    def test_no_dataset(self):
        ''' Verifica se retorna objeto todo nulo se não houver dataset '''
        model = StubModel()
        self.assertEqual(model.wrap_result(None), None)

    def test_valid_dataset(self):
        ''' Verifica se retorna dataset encapsulado corretamente '''
        model = StubModel()

        str_dataset = StringIO(
            """nm_indicador;nu_competencia;vl_indicador
                Ficticio;2099;1
                """
        )
        dataset = pd.read_csv(str_dataset, sep=";")

        str_expected = """{
            "metadata": {
                "fonte": "Instituto STUB"
            },
            "dataset": [
                {
                    "nm_indicador": "Ficticio",
                    "nu_competencia": 2099,
                    "vl_indicador": 1
                }
            ]
        }"""

        result = "".join(model.wrap_result(dataset).split())
        expected = "".join(str_expected.split())
        self.assertEqual(result, expected)

class BaseModelTemplateTest(unittest.TestCase):
    ''' Test behaviours linked to first-tier template interpolation '''
    def test_replace_template_arg(self):
        ''' Test first-tier interpolation '''
        model = StubModel()
        data_collection = {
            "stub": {"col_1": "prop_arg"}
        }
        rules = {
            "template": "One {} {}, two {}, three {}",
            "args": [
                {"as_is": True, "fixed": "asisarg1"},
                {"as_is": True, "fixed": "asisarg2"},
                {"fixed": "fixedarg"},
                {"named_prop": "col_1", "base_object": "stub"}
            ]
        }
        self.assertEqual(
            model.replace_template_arg(rules, data_collection),
            {'fixed': 'One {0} {1}, two fixedarg, three prop_arg'}
        )

    def test_replace_template_arg_keep_template(self):
        ''' Test first-tier interpolation '''
        model = StubModel()
        data_collection = {
            "stub": {"col_1": "prop_arg"}
        }
        rules = {
            "template": "One {} {}, two {}, three {}",
            "keep_template": True,
            "args": [
                {"as_is": True, "fixed": "asisarg1"},
                {"as_is": True, "fixed": "asisarg2"},
                {"fixed": "fixedarg"},
                {"named_prop": "col_1", "base_object": "stub"}
            ]
        }
        self.assertEqual(
            model.replace_template_arg(rules, data_collection),
            {
                "template": 'One {0} {1}, two fixedarg, three prop_arg',
                "args": [{"fixed": "asisarg1"}, {"fixed": "asisarg2"}]
            }
        )

    def test_replace_named_prop(self):
        ''' Test named_prop substitution '''
        model = StubModel()
        data_collection = {
            "stub": {"col_1": 1.23}
        }
        rules = {
            "named_prop": "col_1",
            "base_object": "stub",
            "format": "monetario",
            "precision": 1,
            "multiplier": 2,
            "uiTags": False,
            "collapse": {"format": "inteiro"}
        }
        self.assertEqual(
            model.replace_named_prop(rules, data_collection),
            {"fixed": "R$2,5"}
        )

class BaseModelRunNamedFunctionTest(unittest.TestCase):
    ''' Test functions calls by reflection '''
    def test_run_slice_function(self):
        ''' Test slicing a dataframe object '''
        model = StubModel()
        self.assertEqual(
            model.run_named_function(
                {
                    'function': 'slice',
                    'args': [{"fixed": 0}, {"fixed": 2}]
                },
                range(10)
            ),
            [0, 1]
        )

    def test_run_slice_function_ignore_non_fixed_args(self):
        ''' Test if non-fixed args are ignored correctly '''
        model = StubModel()
        self.assertEqual(
            model.run_named_function(
                {
                    'function': 'slice',
                    'args': [{"fixed": 0}, {"prop": "vals"}, {"fixed": 2}]
                },
                list(range(10))
            ),
            [0, 1]
        )

    def test_run_slice_function(self):
        ''' Test slicing a dataframe object '''
        # Defining a custom class for instantiation
        class CustomClass():
            ''' Creating a class for running its function '''
            vals = list(range(10))
            def fake_slice(self, limit):
                ''' Method to call by reflection '''
                return self.vals[limit:]
        # Running test
        model = StubModel()
        self.assertEqual(
            model.run_named_function(
                {
                    'function': 'fake_slice',
                    'args': [{"fixed": 5}]
                },
                CustomClass()
            ),
            [5, 6, 7, 8, 9]
        )
