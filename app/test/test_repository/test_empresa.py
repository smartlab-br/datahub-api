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
        self.assertEqual(
            StubEmpresaRepository().find_datasets({}),
            None
        )

    def test_find_dataset(self):
        ''' Tests if the dataset is returned correctly '''
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


class EmpresaRepositoryFilterByPersonTest(unittest.TestCase):
    ''' Tests company dataset filtering by person '''
    SOURCE_DATA = pd.DataFrame([
        {
            "cnpj": '12345678000101',
            'nu_cpf': '12345678900',
            'col_compet': 2099
        },
        {
            "cnpj": '12345678000101',
            'nu_cpf': '98765432100',
            'col_compet': 2099
        },
        {
            "cnpj": '12345678000202',
            'nu_cpf': '19283746500',
            'col_compet': 2099
        },
        {
            "cnpj": '12345678000202',
            'nu_cpf': '12345678900',
            'col_compet': 2099
        }
    ])
    def test_filter_by_person_no_data(self):
        ''' Tests if None is returned when no data is sent '''
        self.assertEqual(
            EmpresaRepository().filter_by_person(None, None, None, None), None
        )

    def test_filter_by_person_no_options(self):
        ''' Tests if None is returned when no options are sent '''
        self.assertEqual(
            EmpresaRepository().filter_by_person(self.SOURCE_DATA, None, None, None),
            None
        )

    def test_filter_by_person_no_person_id_column(self):
        ''' Tests if the dataframe is returned AS-IS when no column ID is given
            for the person '''
        self.assertEqual(
            EmpresaRepository().filter_by_person(
                self.SOURCE_DATA, {"id_pf": '12345678900'}, None, None
            ).to_dict(orient="records"),
            self.SOURCE_DATA.to_dict(orient="records")
        )

    def test_filter_by_person(self):
        ''' Tests if the dataframe is filtered correctly '''
        self.assertEqual(
            EmpresaRepository().filter_by_person(
                self.SOURCE_DATA, {"id_pf": '12345678900'}, 'cnpj', 'nu_cpf'
            ).to_dict(orient="records"),
            [
                {
                    "cnpj": '12345678000101',
                    'nu_cpf': '12345678900',
                    'col_compet': 2099
                },
                {
                    "cnpj": '12345678000202',
                    'nu_cpf': '12345678900',
                    'col_compet': 2099
                }
            ]
        )

    def test_filter_by_company(self):
        ''' Tests if the dataframe is filtered correctly '''
        self.assertEqual(
            EmpresaRepository().filter_by_person(
                self.SOURCE_DATA, {"cnpj": '12345678000101'}, 'cnpj', 'nu_cpf'
            ).to_dict(orient="records"),
            [
                {
                    "cnpj": '12345678000101',
                    'nu_cpf': '12345678900',
                    'col_compet': 2099
                },
                {
                    "cnpj": '12345678000101',
                    'nu_cpf': '98765432100',
                    'col_compet': 2099
                }
            ]
        )

    def test_filter_by_person_default_company_id_column(self):
        ''' Tests if the dataframe is filtered correctly '''
        self.assertEqual(
            EmpresaRepository().filter_by_person(
                self.SOURCE_DATA, {"cnpj": '12345678000101'}, None, 'nu_cpf'
            ).to_dict(orient="records"),
            [
                {
                    "cnpj": '12345678000101',
                    'nu_cpf': '12345678900',
                    'col_compet': 2099
                },
                {
                    "cnpj": '12345678000101',
                    'nu_cpf': '98765432100',
                    'col_compet': 2099
                }
            ]
        )

    def test_filter_by_company_and_person(self):
        ''' Tests if the dataframe is filtered correctly '''
        dataframe = self.SOURCE_DATA.copy()
        dataframe = dataframe.rename(columns={"cnpj": "cnpj_cei"})
        self.assertEqual(
            EmpresaRepository().filter_by_person(
                dataframe,
                {"id_pf": '12345678900', "cnpj": '12345678000202'},
                'cnpj_cei',
                'nu_cpf'
            ).to_dict(orient="records"),
            [{
                "cnpj_cei": '12345678000202',
                'nu_cpf': '12345678900',
                'col_compet': 2099
            }]
        )

# @staticmethod
#     def filter_by_person(dataframe, options, col_cnpj_name, col_pf_name):
#         ''' Filter dataframe by person identification, according to options data '''
#         cnpj = options.get('cnpj')
#         id_pf = options.get('id_pf')
#         # Filtrar cnpj e id_pf nos datasets pandas
#         if cnpj is not None and id_pf is not None and col_pf_name is not None:
#             if dataframe[col_cnpj_name].dtype == 'int64':
#                 cnpj = int(cnpj)
#             if dataframe[col_pf_name].dtype == 'int64':
#                 id_pf = int(id_pf)
#             dataframe = dataframe[
#                 (dataframe[col_cnpj_name] == cnpj) & (dataframe[col_pf_name] == id_pf)
#             ]
#         # Filtrar apenas cnpj nos datasets pandas
#         elif cnpj is not None:
#             if dataframe[col_cnpj_name].dtype == 'int64':
#                 cnpj = int(cnpj)
#             dataframe = dataframe[dataframe[col_cnpj_name] == cnpj]
#         # Filtrar apenas id_pf nos datasets pandas
#         elif (id_pf is not None and col_pf_name is not None):
#             if dataframe[col_pf_name].dtype == 'int64':
#                 id_pf = int(id_pf)
#             dataframe = dataframe[dataframe[col_pf_name] == id_pf]
#         return dataframe