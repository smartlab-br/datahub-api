'''Main tests in API'''
import unittest
from test.stubs.pandas_operator import StubPandasOperator
import pandas as pd
from service.pandas_operator import PandasOperator

class PandasOperatorRerankTest(unittest.TestCase):
    ''' Test behaviours linked to reranking dataframes '''
    DATAFRAME_RERANK = pd.DataFrame([
        {
            "cd_indicador": '1',
            "cd_municipio": '111111',
            "cd_uf": '11',
            "agr_sum_vl_indicador": 40
        },
        {
            "cd_indicador": '1',
            "cd_municipio": '111112',
            "cd_uf": '11',
            "agr_sum_vl_indicador": 10
        },
        {
            "cd_indicador": '2',
            "cd_municipio": '111111',
            "cd_uf": '11',
            "agr_sum_vl_indicador": 4
        },
        {
            "cd_indicador": '2',
            "cd_municipio": '211111',
            "cd_uf": '21',
            "agr_sum_vl_indicador": 1
        }
    ])

    EXPECTED_RERANK = [
        {
            "cd_indicador": '1',
            "cd_municipio": '111111',
            "cd_uf": '11',
            "agr_sum_vl_indicador": 40,
            "agr_sum_vl_indicador_br": 50,
            "rerank_rank_br": 1.0,
            "rerank_perc_br": 0.8,
            "agr_sum_vl_indicador_uf": 50,
            "rerank_rank_uf": 1.0,
            "rerank_perc_uf": 0.8
        },
        {
            "cd_indicador": '1',
            "cd_municipio": '111112',
            "cd_uf": '11',
            "agr_sum_vl_indicador": 10,
            "agr_sum_vl_indicador_br": 50,
            "rerank_rank_br": 2.0,
            "rerank_perc_br": 0.2,
            "agr_sum_vl_indicador_uf": 50,
            "rerank_rank_uf": 2.0,
            "rerank_perc_uf": 0.2
        },
        {
            "cd_indicador": '2',
            "cd_municipio": '111111',
            "cd_uf": '11',
            "agr_sum_vl_indicador": 4,
            "agr_sum_vl_indicador_br": 5,
            "rerank_rank_br": 1.0,
            "rerank_perc_br": 0.8,
            "agr_sum_vl_indicador_uf": 4,
            "rerank_rank_uf": 1.0,
            "rerank_perc_uf": 1.0
        },
        {
            "cd_indicador": '2',
            "cd_municipio": '211111',
            "cd_uf": '21',
            "agr_sum_vl_indicador": 1,
            "agr_sum_vl_indicador_br": 5,
            "rerank_rank_br": 2.0,
            "rerank_perc_br": 0.2,
            "agr_sum_vl_indicador_uf": 1,
            "rerank_rank_uf": 1.0,
            "rerank_perc_uf": 1.0
        }
    ]

    def test_rerank(self):
        ''' Tests if data is re-ranked '''
        self.assertEqual(
            PandasOperator.rerank(self.DATAFRAME_RERANK.copy()).to_dict(orient="records"),
            self.EXPECTED_RERANK
        )

    def test_rerank_from_op(self):
        ''' Tests if data is re-ranked '''
        self.assertEqual(
            StubPandasOperator.operate(
                self.DATAFRAME_RERANK.copy(),
                'rerank',
                [
                    "cd_indicador", "cd_municipio", "cd_uf", "agr_sum_vl_indicador",
                    "agr_sum_vl_indicador_br", "rerank_rank_br", "rerank_perc_br",
                    "agr_sum_vl_indicador_uf", "rerank_rank_uf", "rerank_perc_uf"
                ]
            ).to_dict(orient="records"),
            self.EXPECTED_RERANK
        )

class PandasOperatorCutTest(unittest.TestCase):
    ''' Test behaviours linked to reranking dataframes '''
    DATAFRAME_CUT = pd.DataFrame([
        {"idade": 10, "agr_count": 25},
        {"idade": 15, "agr_count": 25},
        {"idade": 20, "agr_count": 35},
        {"idade": 25, "agr_count": 50},
        {"idade": 30, "agr_count": 100},
        {"idade": 35, "agr_count": 43},
        {"idade": 60, "agr_count": 12}
    ])

    def test_cut_right_exclude(self):
        ''' Tests if data is cut with open left member '''
        expected = [
            {"row_id": 0, "cut": 'a', "agr_count": 50},
            {"row_id": 1, "cut": 'b', "agr_count": 228},
            {"row_id": 2, "cut": 'c', "agr_count": 12}
        ]

        self.assertEqual(
            PandasOperator.cut(
                self.DATAFRAME_CUT.copy(),
                'idade',
                {'bins': [0, 18, 60, 100], 'right': False, 'labels': ['a', 'b', 'c']},
                ['idade']
            ).to_dict(orient="records"),
            expected
        )

    def test_cut(self):
        ''' Tests if data is cut with closed right member '''
        expected = [
            {"row_id": 0, "cut": 'a', "agr_count": 50},
            {"row_id": 1, "cut": 'b', "agr_count": 240},
            {"row_id": 2, "cut": 'c', "agr_count": 0}
        ]

        self.assertEqual(
            PandasOperator.cut(
                self.DATAFRAME_CUT.copy(),
                'idade',
                {'bins': [0, 18, 60, 100], 'right': True, 'labels': ['a', 'b', 'c']},
                ['idade']
            ).to_dict(orient="records"),
            expected
        )

    def test_cut_from_op(self):
        ''' Tests if data is cut correctly from operate function '''
        expected = [
            {"row_id": 0, "cut": 'a', "agr_count": 50},
            {"row_id": 1, "cut": 'b', "agr_count": 228},
            {"row_id": 2, "cut": 'c', "agr_count": 12}
        ]

        self.assertEqual(
            StubPandasOperator.operate(
                self.DATAFRAME_CUT.copy(),
                'cut-idade',
                ["idade"]
            ).to_dict(orient="records"),
            expected
        )

    def test_cut_from_op_no_target(self):
        ''' Tests if data is returned AS-IS if no pattern is sent to operate '''
        self.assertEqual(
            StubPandasOperator.operate(
                self.DATAFRAME_CUT.copy(),
                'cut',
                ["idade"]
            ).to_dict(orient="records"),
            self.DATAFRAME_CUT.copy().to_dict(orient="records")
        )

    def test_cut_from_op_pattern(self):
        ''' Tests if data is re-ranked '''
        expected = [
            {"row_id": 0, "cut": 'a', "agr_count": 278},
            {"row_id": 1, "cut": 'b', "agr_count": 12}
        ]

        self.assertEqual(
            StubPandasOperator.operate(
                self.DATAFRAME_CUT.copy(),
                'cut-idade-ptrn',
                ["idade"]
            ).to_dict(orient="records"),
            expected
        )
