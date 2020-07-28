'''Main tests in API'''
import unittest
import pandas as pd
from repository.empresa.empresa import EmpresaRepository

class StubEmpresaRepository(EmpresaRepository):
    ''' Stub repository to leverage testing '''
    SOURCE_DATA = [
        {
            "nu_cnpj_cei": '12345678000101',
            'nu_cpf': '12345678900',
            'col_compet': 2099,
            'origem_busca': 'Empregador'
        },
        {
            "nu_cnpj_cei": '12345678000202',
            'nu_cpf': '12345678900',
            'col_compet': 2099,
            'origem_busca': 'Tomador'
        },
        {
            "nu_cnpj_cei": '12345678000303',
            'nu_cpf': '12345678900',
            'col_compet': 2099,
            'origem_busca': 'Empregador Concessão'
        },
        {
            "nu_cnpj_cei": '12345678000404',
            'nu_cpf': '12345678900',
            'col_compet': 2099,
            'origem_busca': 'Empregador AEPS'
        }
    ]
    EXPECTED_RESULT = {
        'catweb_empregador': [
            {
                'nu_cnpj_cei': '12345678000101',
                'nu_cpf': '12345678900',
                'col_compet': 2099,
                'origem_busca': 'Empregador'
            }
        ],
        'catweb_tomador': [
            {
                'nu_cnpj_cei': '12345678000202',
                'nu_cpf': '12345678900',
                'col_compet': 2099,
                'origem_busca': 'Tomador'
            }
        ],
        'catweb_concessao': [
            {
                'nu_cnpj_cei': '12345678000303', 
                'nu_cpf': '12345678900',
                'col_compet': 2099,
                'origem_busca': 'Empregador Concessão'
                }
        ],
        'catweb_aeps': [
            {
                'nu_cnpj_cei': '12345678000404',
                'nu_cpf': '12345678900',
                'col_compet': 2099,
                'origem_busca': 'Empregador AEPS'
            }
        ]
    }
    def load_and_prepare(self):
        ''' Overriding to avoid application context requirement '''

    def find_row(self, table, row, column_family, column):
        return {
            "rfb": pd.DataFrame([
                {
                    'nu_cnpj_cei': '12345678000101',
                    'nu_cpf': '12345678900',
                    'col_compet': 2099
                }
            ]),
            'catweb': pd.DataFrame(self.SOURCE_DATA)
        }

class EmpresaRepositorySplitDataframePerspectiveTest(unittest.TestCase):
    ''' Tests dataset splitting by perspectives '''
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
        result = EmpresaRepository().split_dataframe_by_perspective(
            {"catweb": pd.DataFrame(StubEmpresaRepository.SOURCE_DATA)}, {}
        )
        for k, v in StubEmpresaRepository.EXPECTED_RESULT.items():
            self.assertEqual(result.get(k).to_dict(orient="records"),v)

    def test_splitting_single_perspective(self):
        ''' Tests if data is split correctly when a perspective is given '''
        result = EmpresaRepository().split_dataframe_by_perspective(
            {"catweb": pd.DataFrame(StubEmpresaRepository.SOURCE_DATA)},
            {'perspective': 'empregador'}
        )
        expected = {
            "catweb_empregador": StubEmpresaRepository.EXPECTED_RESULT.get('catweb_empregador')
        }
        for k, v in expected.items():
            self.assertEqual(result.get(k).to_dict(orient="records"),v)

    def test_splitting_mixed(self):
        ''' Tests if data is split correctly when data contains both a simple
            dataset and a splittable one '''
        result = EmpresaRepository().split_dataframe_by_perspective({
            "rfb": pd.DataFrame([{"cnpj_raiz": '12345678'}]),
            "catweb": pd.DataFrame(StubEmpresaRepository.SOURCE_DATA)
        }, {})
        for k, v in StubEmpresaRepository.EXPECTED_RESULT.items():
            self.assertEqual(result.get(k).to_dict(orient="records"),v)

class EmpresaRepositoryFindDatasetTest(unittest.TestCase):
    ''' Tests dataset splitting by perspectives '''
    def test_find_dataset_no_options(self):
        ''' Tests if None is returned when no options are sent '''
        self.assertEqual(StubEmpresaRepository().find_datasets(None), None)

    def test_find_dataset_empty_options(self):
        ''' Tests if None is returned when empty options are sent '''
        self.maxDiff = None
        self.assertEqual(
            StubEmpresaRepository().find_datasets({}),
            None
        )

    def test_find_dataset(self):
        ''' Tests if the dataset is returned correctly '''
        self.maxDiff = None
        self.assertEqual(
            StubEmpresaRepository().find_datasets({'cnpj_raiz': '12345678'}),
            {
                **{"catweb": StubEmpresaRepository.SOURCE_DATA},
                **StubEmpresaRepository.EXPECTED_RESULT,
                **{"rfb": [
                    {
                        'nu_cnpj_cei': '12345678000101',
                        'nu_cpf': '12345678900',
                        'col_compet': 2099
                    }
                ]}
            }
        )

    def test_find_dataset_simplified(self):
        ''' Tests if a smaller version of dataset is returned, with fewer columns '''
        self.assertEqual(
            StubEmpresaRepository().find_datasets({'cnpj_raiz': '12345678', 'simplified': True}),
            {
                'catweb': [
                    {
                        'nu_cnpj_cei': '12345678000101',
                        'nu_cpf': '12345678900',
                        'col_compet': 2099
                    },
                    {
                        'nu_cnpj_cei': '12345678000202',
                        'nu_cpf': '12345678900',
                        'col_compet': 2099
                    },
                    {
                        'nu_cnpj_cei': '12345678000303', 
                        'nu_cpf': '12345678900',
                        'col_compet': 2099
                    },
                    {
                        'nu_cnpj_cei': '12345678000404',
                        'nu_cpf': '12345678900',
                        'col_compet': 2099
                    }
                ],
                'catweb_empregador': [
                    {
                        'nu_cnpj_cei': '12345678000101',
                        'nu_cpf': '12345678900',
                        'col_compet': 2099
                    }
                ],
                'catweb_tomador': [
                    {
                        'nu_cnpj_cei': '12345678000202',
                        'nu_cpf': '12345678900',
                        'col_compet': 2099
                    }
                ],
                'catweb_concessao': [
                    {
                        'nu_cnpj_cei': '12345678000303', 
                        'nu_cpf': '12345678900',
                        'col_compet': 2099
                    }
                ],
                'catweb_aeps': [
                    {
                        'nu_cnpj_cei': '12345678000404',
                        'nu_cpf': '12345678900',
                        'col_compet': 2099
                    }
                ],
                "rfb": [
                    {
                        'nu_cnpj_cei': '12345678000101',
                        'nu_cpf': '12345678900',
                        'col_compet': 2099
                    }
                ]
            }
        )
# def find_datasets(self, options):
#         ''' Localiza um município pelo código do IBGE '''
#         if 'cnpj_raiz' not in options or options['cnpj_raiz'] is None:
#             return None

#         result = self.find_row(
#             'empresa',
#             options['cnpj_raiz'],
#             options.get('column_family'),
#             options.get('column')
#         )

#         # Result splitting according to perspectives
#         result = {**result, **self.split_dataframe_by_perspective(result, options)}

#         for ds_key in result:
#             col_cnpj_name = self.CNPJ_COLUMNS.get(ds_key, 'cnpj')
#             col_pf_name = self.PF_COLUMNS.get(ds_key)

#             if not result[ds_key].empty:
#                 result[ds_key] = self.filter_by_person(
#                     result[ds_key], options, col_cnpj_name, col_pf_name
#                 )

#             # Redução de dimensionalidade (simplified)
#             if not result[ds_key].empty and options.get('simplified'):
#                 list_dimred = self.SIMPLE_COLUMNS.get(
#                     ds_key, ['nu_cnpj_cei', 'nu_cpf', 'col_compet']
#                 )
#                 # Garantir que col_compet sempre estará na lista
#                 if 'col_compet' not in list_dimred:
#                     list_dimred.append('col_compet')
#                 result[ds_key] = result[ds_key][list_dimred]

#             # Conversão dos datasets em json
#             result[ds_key] = json.loads(result[ds_key].to_json(orient="records"))
#         return result
