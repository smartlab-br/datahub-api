'''Main tests in API'''
import unittest

def test_one():
    '''Teste do teste'''
    pass

class TestClass(unittest.TestCase):
    '''Classe de testes'''
    def test_example(self):
        '''Testa se 1 = 1'''
        self.assertEqual(1, 1)
