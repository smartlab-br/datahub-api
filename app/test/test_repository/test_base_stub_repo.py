
'''Main tests in API'''
import unittest
from test.stubs.repository import StubRepository

class BaseRepositoryGeneralTest(unittest.TestCase):
    ''' General tests over StubRepo '''
    def test_table_name(self):
        ''' Verifica correta obtenção de nome de tabela '''
        repo = StubRepository()
        tbl_name = repo.get_table_name('MAIN')
        self.assertEqual(tbl_name, 'indicadores')

class BaseRepositoryLoadAndPrepareTest(unittest.TestCase):
    ''' Classe que testa o carregamento do dao '''
    def test_valid(self):
        ''' Verifica declaração do método de carregamento do dao. '''
        repo = StubRepository()
        self.assertEqual(repo.get_dao(), 'Instanciei o DAO')
