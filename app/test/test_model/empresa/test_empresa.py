'''Main tests in API'''
import unittest
from model.empresa.empresa import Empresa
from test.stubs.empresa import StubEmpresa

class EmpresaModelBaseTest(unittest.TestCase):
    ''' Classe que testa o mapeamento de agregações para funções do pandas '''
    def test_default_on_none(self):
        ''' Verifica se retorna np.mean se agregação nula '''
        self.assertEqual(
            Empresa().get_stats_local_options(
                {
                    'column': 2099,
                    'cnpj_raiz': '12345678',
                    'cnpj': '12345678000101',
                    'id_pf': '12345678900'
                },
                {
                    'compet': 'col_compet',
                    'cnpj_raiz': 'col_cnpj_raiz',
                    'cnpj_raiz_flag': 'flag', 'cnpj': 'cnpj_col',
                    'cnpj_flag': 'flag_2', 'pf': 'pf_col'
                },
                'theme',
                None
            ),
            {
                'categorias': ['col_cnpj_raiz'],
                'agregacao': ['count'],
                'where': [
                    "eq-col_cnpj_raiz-12345678",
                    "and", "eq-flag-'1'",
                    "and", "eq-cnpj_col-12345678000101",
                    "and", "eq-flag_2-'1'",
                    "and", "eq-pf_col-12345678900"
                ],
                'theme': 'theme'
            }
        )

    def test_build_empty_stats_no_aggr(self):
        ''' Tests if a 0 total object is created according to given options with
            no aggregations '''
        self.assertEqual(
            Empresa.build_empty_stats(
                {},
                {"cnpj_raiz": "col_cnpj_raiz"},
                {"cnpj_raiz": "12345678"}
            ),
            {"col_cnpj_raiz": "12345678"}
        )

    def test_build_empty_stats_aggr(self):
        ''' Tests if a 0 total object is created according to given options with
            aggregations '''
        self.assertEqual(
            Empresa.build_empty_stats(
                {"agregacao": ['sum', 'count']},
                {"cnpj_raiz": "col_cnpj_raiz"},
                {"cnpj_raiz": "12345678"}
            ),
            {
                "col_cnpj_raiz": "12345678",
                "agr_sum": 0,
                "agr_count": 0
            }
        )

    def test_build_empty_stats_val_aggr(self):
        ''' Tests if a 0 total object is created according to given options with
            aggregations and values '''
        self.assertEqual(
            Empresa.build_empty_stats(
                {"agregacao": ['sum', 'count'], "valor": ['vl_a', 'vl_b']},
                {"cnpj_raiz": "col_cnpj_raiz"},
                {"cnpj_raiz": "12345678"}
            ),
            {
                "col_cnpj_raiz": "12345678",
                "agr_sum_vl_a": 0, "agr_count_vl_a": 0,
                "agr_sum_vl_b": 0, "agr_count_vl_b": 0
            }
        )

class AssessColumnStatusTest(unittest.TestCase):
    ''' Class to test the status assessmente from a collection of status
        keys retrieved from REDIS '''
    SLOT_LIST = ['2019', '2020', '2047']
    KEY_COLLECTION = {'2019': 'INGESTED', '2020': 'INGESTING', '2099': 'INGESTED'}

    def test_assess_column_status_existing(self):
        ''' Tests if the existing column status is returned correctly '''
        self.assertEqual(
            Empresa.assess_column_status(self.SLOT_LIST, self.KEY_COLLECTION, '2019'),
            'INGESTED'
        )

    def test_assess_column_status_missing(self):
        ''' Tests if the missing column status is returned correctly when
            the column exists in the list but not in the collection from REDIS '''
        self.assertEqual(
            Empresa.assess_column_status(self.SLOT_LIST, self.KEY_COLLECTION, '2047'),
            'MISSING'
        )

    def test_assess_column_status_deprecated(self):
        ''' Tests if the deprecated data status is returned correctly when
            the column exists in the collection from REDIS but not in the
            dictionary of data present in datalake '''
        self.assertEqual(
            Empresa.assess_column_status(self.SLOT_LIST, self.KEY_COLLECTION, '2099'),
            'DEPRECATED'
        )

    def test_assess_column_status_unavailable(self):
        ''' Tests if the unavailable column status is returned correctly
            when a data that is not present both in the dictionary of
            available data and the REDIS collection '''
        self.assertEqual(
            Empresa.assess_column_status(self.SLOT_LIST, self.KEY_COLLECTION, '1500'),
            'UNAVAILABLE'
        )

class StubGetGroupedStatsTest(unittest.TestCase):
    ''' Tests the grouped statistics fetching using static data as source '''
    def test_get_grouped_stats(self):
        ''' Tests basic grouped stats retrieval '''
        self.assertEqual(
            StubEmpresa().get_grouped_stats(
                {},
                {'theme': 'mytheme'},
                {}
            ),
            {
                'stats_estab': {
                    '12345678000101': {'agr_count': 100, 'compet': 2047},
                    '12345678000202': {'agr_count': 200, 'compet': 2099}
                },
                'stats_compet': {
                    '2047': {'agr_count': 100, 'cnpj': '12345678000101'},
                    '2099': {'agr_count': 200, 'cnpj': '12345678000202'}
                },
                'stats_estab_compet': {
                    '2047_12345678000101': {
                        'agr_count': 100, 'cnpj': '12345678000101', 'compet': 2047
                    },
                    '2099_12345678000202': {
                        'agr_count': 200, 'cnpj': '12345678000202', 'compet': 2099
                    }
                }
            }
        )

    def test_get_grouped_stats_displaced_compet_alt(self):
        ''' Tests basic grouped stats retrieval '''
        self.assertEqual(
            StubEmpresa().get_grouped_stats(
                {},
                {'theme': 'catewb'},
                {}
            ),
            {
                'stats_estab': {
                    '12345678000101': {'agr_count': 100, 'compet': 2047},
                    '12345678000202': {'agr_count': 200, 'compet': 2099}
                },
                'stats_compet': {
                    '2047': {'agr_count': 100, 'cnpj': '12345678000101'},
                    '2099': {'agr_count': 200, 'cnpj': '12345678000202'}
                },
                'stats_estab_compet': {
                    '2047_12345678000101': {
                        'agr_count': 100, 'cnpj': '12345678000101', 'compet': 2047
                    },
                    '2099_12345678000202': {
                        'agr_count': 200, 'cnpj': '12345678000202', 'compet': 2099
                    }
                }
            }
        )

# def get_grouped_stats(self, original_options, options, cols):
#         ''' Get stats for dataframe partitions '''
#         result = {}
#         options['as_pandas'] = True
#         options['no_wrap'] = True
#         # Get statistics partitioning by unit
#         if 'cnpj' not in cols: # Ignores datasources with no cnpj definition
#             result["stats_estab"] = json.loads(
#                 self.get_thematic_handler().find_dataset({
#                     **options,
#                     **{
#                         "categorias": [cols.get('cnpj')],
#                         "ordenacao": [cols.get('cnpj')]
#                     }
#                 }).set_index(cols.get('cnpj')).to_json(orient="index")
#             )
#         # Get statistics partitioning by timeframe
#         ds_no_compet = [
#             'sisben', 'sisben_c', 'auto', 'rfb', 'rfbsocios',
#             'rfbparticipacaosocietaria', 'aeronaves', 'renavam'
#         ]
#         ds_displaced_compet = ['catweb', 'catweb_c']
#         # Ignores datasources with no timeframe definition
#         if options.get('theme') not in ds_no_compet:
#             # Get statistics partitioning by timeframe
#             compet_attrib = 'compet' # Single timeframe, no need to group
#             if 'compet' in cols and options.get('theme') not in ds_displaced_compet:
#                 # Changes lookup for tables with timeframe values
#                 compet_attrib = cols.get('compet')
#                 current_df = self.get_thematic_handler.find_dataset({
#                     **options,
#                     **{
#                         "categorias": [compet_attrib],
#                         "ordenacao":[f"-{compet_attrib}"]
#                     }
#                 })
#             else:
#                 current_df = self.get_thematic_handler.find_dataset({
#                     **options,
#                     **{
#                         "categorias": [f"\'{original_options.get('column')}\'-compet"],
#                         "ordenacao": ["-compet"]
#                     }
#                 })
#             current_df[compet_attrib] = current_df[compet_attrib].apply(str).replace(
#                 {'\.0': ''}, regex=True
#             )
#             result["stats_compet"] = json.loads(
#                 current_df.set_index(compet_attrib).to_json(orient="index")
#             )
#             # Get statistics partitioning by timeframe and units
#             if 'compet' in cols and options.get('theme') not in ds_displaced_compet:
#                 # Changes lookup for tables with timeframe values
#                 df_local_result = self.get_thematic_handler.find_dataset({
#                     **options,
#                     **{"categorias": [cols.get('cnpj'), compet_attrib]}
#                 })
#             else:
#                 df_local_result = self.get_thematic_handler.find_dataset({
#                     **options,
#                     **{
#                         "categorias": [cols.get('cnpj'),
#                         f"\'{original_options.get('column')}\'-compet"]
#                     }
#                 })
#             df_local_result['idx'] = df_local_result[compet_attrib].apply(str).replace(
#                 {'\.0': ''}, regex=True) + '_' + \
#                 df_local_result[cols.get('cnpj')].apply(str).replace({'\.0': ''}, regex=True)
#             result["stats_estab_compet"] = json.loads(
#                 df_local_result.set_index('idx').to_json(orient="index")
#             )
#         ## RETIRADO pois a granularidade torna imviável a performance
#         # metadata['stats_pf'] = dataframe[
#         #     [col_pf_name, 'col_compet']
#         # ].groupby(col_pf_name).describe(include='all')
#         ## RETIRADO pois a granularidade torna inviável a performance
#         # metadata['stats_pf_compet'] = dataframe[
#         #     [col_pf_name, 'col_compet']
#         # ].groupby(
#         #     ['col_compet', col_cnpj_name]
#         # ).describe(include='all')
#         return result