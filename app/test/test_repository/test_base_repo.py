"""Main tests in API"""
import unittest
from test.stubs.repository import StubRepository, StubNoLoadRepository, StubHadoopRepository, StubNoLoadHadoopRepository


class BaseRepositoryInstantiationTest(unittest.TestCase):
    """ Tests instantiation errors """
    def test_invalid_load(self):
        """ Verifica lançamento de exceção ao instanciar classe sem
            implementação de load_and_prepare. """
        self.assertRaises(NotImplementedError, StubNoLoadRepository)

    def test_decode_colum_defs(self):
        """ Tests if the column definitions are correctly loaded according
            to given perspective """
        column_defs = {
            'cnpj_raiz': {
                'persp_a': {'column': 'col_raiz_a', "flag": True},
                'persp_b': {'column': 'col_raiz_b', "flag": False}
            },
            'cnpj': {
                'persp_a': {'column': 'col_cnpj_a', "flag": True},
                'persp_b': {'column': 'col_cnpj_b', "flag": False}
            }
        }
        self.assertEqual(
            StubRepository.decode_column_defs(column_defs, 'persp_a'),
            {
                'cnpj_raiz': 'col_raiz_a', 'cnpj_raiz_flag': True,
                'cnpj': 'col_cnpj_a', 'cnpj_flag': True
            }
        )

class HadoopRepositoryBuildComplexCriteriaTest(unittest.TestCase):
    """ Tests complex criteria string builder """
    SIMPLE_OPERATORS = {
        'EQ': "=", "NE": "!=", "LE": "<=", "LT": "<", "GE": ">=",
        "GT": ">", "LK": "LIKE", "NL": "NOT LIKE"
    }
    def test_invalid_load(self):
        """ Verifica lançamento de exceção ao instanciar classe sem
            implementação de load_and_prepare. """
        self.assertRaises(NotImplementedError, StubNoLoadHadoopRepository)

    def test_on_criteria(self):
        """ Tests only_numbers criteria """
        w_clause = ['eqon', 'column', 'value']
        self.assertEqual(
            StubHadoopRepository.build_complex_criteria(w_clause, self.SIMPLE_OPERATORS),
            "regexp_replace(CAST(column AS STRING), '[^[:digit:]]','') = 'value'"
        )

    def test_on_criteria_substring(self):
        """ Tests only_numbers criteria with substring """
        w_clause = ['eqon', 'column', 'value', 'slice_start', 'slice_end']
        self.assertEqual(
            StubHadoopRepository.build_complex_criteria(w_clause, self.SIMPLE_OPERATORS),
            "substring(regexp_replace(CAST(column AS STRING), "
            "'[^[:digit:]]',''), slice_start, slice_end) = 'value'"
        )

    def test_lponstr_criteria(self):
        """ Tests only_numbers_against_string criteria with left padding """
        w_clause = ['nelponstr', 'column', 'value']
        self.assertEqual(
            StubHadoopRepository.build_complex_criteria(w_clause, self.SIMPLE_OPERATORS),
            "regexp_replace(CAST(column AS STRING), '[^[:digit:]]','') != 'value'"
        )

    def test_lponstr_criteria_substring(self):
        """ Tests only_numbers_against_string criteria with left padding """
        w_clause = [
            'nelponstr', 'column', 'value', 'string_size', 'padding_char',
            'slice_start', 'slice_end'
        ]
        self.assertEqual(
            StubHadoopRepository.build_complex_criteria(w_clause, self.SIMPLE_OPERATORS),
            "substring(LPAD(regexp_replace(CAST(column AS STRING), "
            "'[^[:digit:]]',''), string_size, 'padding_char'), slice_start, slice_end) "
            "!= 'value'"
        )

    def test_str_criteria(self):
        """ Tests substrings comparison criteria """
        w_clause = ['lestr', 'column', "'quoted_value'", 'slice_start', 'slice_end']
        self.assertEqual(
            StubHadoopRepository.build_complex_criteria(w_clause, self.SIMPLE_OPERATORS),
            "substring(CAST(column AS STRING), slice_start, slice_end) <= 'quoted_value'"
        )

    def test_lpstr_criteria(self):
        """ Tests string with left padding comparison criteria """
        w_clause = [
            'gelpstr', 'column', "'quoted_value'", 'string_size', 'padding_char',
            'slice_start', 'slice_end'
        ]
        self.assertEqual(
            StubHadoopRepository.build_complex_criteria(w_clause, self.SIMPLE_OPERATORS),
            "substring(LPAD(CAST(column AS VARCHAR(string_size)), "
            "string_size, 'padding_char'), slice_start, slice_end) >= 'quoted_value'"
        )

    def test_lpint_criteria(self):
        """ Tests integer with left padding comparison criteria """
        w_clause = [
            'gtlpint', 'column', 'value', 'string_size', 'padding_char',
            'slice_start', 'slice_end'
        ]
        self.assertEqual(
            StubHadoopRepository.build_complex_criteria(w_clause, self.SIMPLE_OPERATORS),
            "CAST(substring(LPAD(CAST(column AS VARCHAR(string_size)), "
            "string_size, 'padding_char'), slice_start, slice_end) AS INTEGER) > value"
        )

    def test_sz_criteria(self):
        """ Tests string size comparison criteria """
        w_clause = ['ltsz', 'column', 'value']
        self.assertEqual(
            StubHadoopRepository.build_complex_criteria(w_clause, self.SIMPLE_OPERATORS),
            "LENGTH(CAST(column AS STRING)) < value"
        )
