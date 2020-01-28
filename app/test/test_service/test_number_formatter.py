''' Testes do formatador '''
import unittest
from service.number_formatter import NumberFormatter

class NumberFormatterTest(unittest.TestCase):
    ''' Classe que testa a formatação de números '''
    def test_pt_inteiro(self):
        ''' Verifica se a formatação de inteiro em pt_br está correta '''
        fmt = NumberFormatter.format(
            2019,
            {"format": 'inteiro', "str_locale": 'pt_br'}
        )
        self.assertEqual(fmt, "2.019")

    def test_en_inteiro(self):
        ''' Verifica se a formatação de inteiro em en está correta '''
        fmt = NumberFormatter.format(
            2019,
            {"format": 'inteiro', "str_locale": 'en'}
        )
        self.assertEqual(fmt, "2,019")

    def test_pt_percentual(self):
        ''' Verifica se a formatação de percentual em pt_br está correta '''
        fmt = NumberFormatter.format(
            53.481,
            {"format": 'porcentagem', "str_locale": 'pt_br'}
        )
        self.assertEqual(fmt, "53,5<span>%</span>")

    def test_pt_real(self):
        ''' Verifica se a formatação de real em pt_br está correta '''
        fmt = NumberFormatter.format(
            53.481,
            {"format": 'real', "str_locale": 'pt_br'}
        )
        self.assertEqual(fmt, "53")

    def test_pt_real_precision(self):
        ''' Verifica se a formatação de real em pt_br está correta '''
        fmt = NumberFormatter.format(
            53.481,
            {"format": 'real', "str_locale": 'pt_br', "precision": 3}
        )
        self.assertEqual(fmt, "53,481")

    def test_pt_collapsed(self):
        ''' Verifica se a formatação de número colapsado em pt_br está correta '''
        fmt = NumberFormatter.format(
            53481,
            {
                "format": 'real',
                "collapse": {"format": "real"},
                "str_locale": 'pt_br'
            }
        )
        self.assertEqual(fmt, "53,5<span>mil</span>")

    def test_pt_collapsed_precision(self):
        ''' Verifica se a formatação de número colapsado em pt_br com precisáo está correta '''
        fmt = NumberFormatter.format(
            53481,
            {
                "format": 'real',
                "collapse": {"format": "real", "precision":1},
                "str_locale": 'pt_br',
                "precision": 1
            }
        )
        self.assertEqual(fmt, "53,5<span>mil</span>")

    def test_dinheiro_pt(self):
        ''' Verifica se a formatação de dinheiro em pt_br está correta '''
        fmt = NumberFormatter.format(
            53481,
            {"format": 'monetario', "str_locale": 'pt_br', "precision": 1}
        )
        self.assertEqual(fmt, "<span>R$</span>53.481")

    def test_dinheiro_pt_no_precision(self):
        ''' Verifica se a formatação de dinheiro com precisão em pt_br está correta '''
        fmt = NumberFormatter.format(
            53481.583,
            {"format": 'monetario', "str_locale": 'pt_br', "precision": 1}
        )
        self.assertEqual(fmt, "<span>R$</span>53.481,6")

    def test_no_valor_with_no_default(self):
        ''' Verifica se retorna '-' quando não há nem valor nem default '''
        fmt = NumberFormatter.format(None, {})
        self.assertEqual(fmt, "-")

    def test_no_valor_with_default(self):
        ''' Verifica se retorna default quando não há valor '''
        fmt = NumberFormatter.format(None, {"default": "N/A"})
        self.assertEqual(fmt, "N/A")

    def test_valor_with_no_format(self):
        ''' Verifica se retorna o próprio valor quando não há definição de formato '''
        fmt = NumberFormatter.format(99, {})
        self.assertEqual(fmt, 99)

    def test_custom_options(self):
        ''' Verifica se retorna os parâmetros customizados corretamente '''
        (
            precision,
            multiplier,
            collapse,
            str_locale,
            _n_format,
            ui_tags
        ) = NumberFormatter.load_defaults({
            "precision": 4,
            "multiplier": 5,
            "collapse": True,
            "str_locale": "en",
            "uiTags": False,
            "format": "real"
        })

        self.assertEqual(precision, 4)
        self.assertEqual(multiplier, 5)
        self.assertEqual(collapse, True)
        self.assertEqual(str_locale, "en")
        self.assertEqual(ui_tags, False)

    def test_monetario_no_tags(self):
        ''' Verifica se retorna 'R$' no prefixo quando não houver tag '''
        prefix = NumberFormatter.get_unit_prefix('monetario', False)
        self.assertEqual(prefix, 'R$')

    def test_multiplying_string(self):
        ''' Verifica se multiplica corretamente quando os parâmetros são strings '''
        fmt = NumberFormatter.apply_multiplier('2', '2')
        self.assertEqual(fmt, 4)

    def test_suffix_percent_no_tags(self):
        ''' Verifica se retorna os sufixos corretamente - percentual sem tag '''
        (_valor, suffix_string, _order_magnitude) = NumberFormatter.get_value_suffix(
            98.76, 'porcentagem', {}, False
        )
        self.assertEqual(suffix_string, '%')

    def test_suffix_collapse_no_tags(self):
        ''' Verifica se retorna os sufixos corretamente - collapsed with no tags'''
        (_valor, suffix_string, _order_magnitude) = NumberFormatter.get_value_suffix(
            10000,
            'inteiro',
            {"format": 'real', "precision": 1, "uiTags": False},
            True
        )
        self.assertEqual(suffix_string, 'mil')

    def test_integer_after_collapse_with_collapse(self):
        ''' Verifica se a avaliação de valor inteiro funciona após o collapse '''
        self.assertTrue(
            NumberFormatter.is_integer_after_collapse(
                'real',
                10000,
                10.0,
                1,
                {"format": 'real', "precision": 1, "uiTags": False},
            )
        )

    def test_pt_collapsed_no_tags(self):
        ''' Verifica se a formatação de número colapsado em pt_br está correta '''
        fmt = NumberFormatter.format(
            53481,
            {
                "format": 'real',
                "collapse": {"format": "real", "uiTags": False},
                "str_locale": 'pt_br'
            }
        )
        self.assertEqual(fmt, "53,5mil")

    def test_validate_as_is(self):
        ''' Verifica se retorna o mesmo valor se for algo válido '''
        num = 12.34
        self.assertEqual(NumberFormatter.validate(num), num)

    def test_valid_float_value_as_string(self):
        ''' Verifica se retorna o valor da string convertido para float '''
        fmt = NumberFormatter.validate("53481.0")
        self.assertEqual(fmt, 53481.0)

    def test_valid_int_value_as_string(self):
        ''' Verifica se retorna o valor da string inteira convertido para float '''
        fmt = NumberFormatter.validate("53481")
        self.assertEqual(fmt, 53481.0)

    def test_invalid_string(self):
        ''' Verifica se erro é lançado quando o valor for uma string não numérica '''
        self.assertRaises(
            ValueError,
            NumberFormatter.validate,
            "a"
        )

    def test_validate_no_value(self):
        ''' Verifica se erro é lançado quando nenhum valor é enviado '''
        self.assertRaises(
            ValueError,
            NumberFormatter.validate,
            None
        )

    def test_validate_nan_value(self):
        ''' Verifica se erro é lançado quando um valor NaN é enviado '''
        self.assertRaises(
            ValueError,
            NumberFormatter.validate,
            float('nan')
        )
