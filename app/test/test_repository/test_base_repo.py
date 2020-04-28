'''Main tests in API'''
import unittest
from repository.base import BaseRepository

class BaseRepositoryInstantiationTest(unittest.TestCase):
    ''' Tests instantiation errors '''
    def test_invalid_load(self):
        ''' Verifica lançamento de exceção ao instanciar classe sem
            implementação de load_and_prepare. '''
        self.assertRaises(NotImplementedError, BaseRepository)
