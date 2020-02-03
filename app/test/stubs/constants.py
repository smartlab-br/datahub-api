''' Constants used in stub classes '''
import pandas as pd

COMMON_EXPECTED_RESPONSE_STRING = """{{
    "metadata": {{"fonte": "Instituto STUB"}},
    "dataset": [{{{0}}}]
    }}"""

COMMON_OPTIONS = {
    "valor": ['vl_indicador'],
    "agregacao": ['sum'],
    "ordenacao": ['-nm_indicador'],
    "where": ['eq-nu_competencia-2010'],
    "joined": None,
}

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
