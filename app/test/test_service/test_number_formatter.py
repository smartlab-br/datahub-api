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
            { "format": 'porcentagem', "str_locale": 'pt_br'}
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
