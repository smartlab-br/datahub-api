''' Constants used in stub classes '''
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
