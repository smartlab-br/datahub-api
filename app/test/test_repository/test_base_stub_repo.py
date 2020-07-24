
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

    def test_table_name_invalid(self):
        ''' Tests if an error is raised when the table name is
            not found in the available collection '''
        self.assertRaises(
            KeyError,
            StubRepository().get_table_name,
            'MISSING'
        )

class BaseRepositoryLoadAndPrepareTest(unittest.TestCase):
    ''' Classe que testa o carregamento do dao '''
    def test_valid(self):
        ''' Verifica declaração do método de carregamento do dao. '''
        repo = StubRepository()
        self.assertEqual(repo.get_dao(), 'Instanciei o DAO')

class BaseRepositoryNamedQueryTest(unittest.TestCase):
    ''' Validates recovery of named query '''
    def test_validate_positive(self):
        ''' Verifica correta obtenção de named query '''
        self.assertEqual(
            StubRepository().NAMED_QUERIES.get('QRY_FIND_DATASET'),
            'SELECT {} FROM {} {} {} {}'
        )

    def test_validate_negative(self):
        ''' Verifica comportamento de obtenção de named query não mapeada '''
        self.assertEqual(StubRepository().NAMED_QUERIES.get('FAKE_QUERY'), None)
