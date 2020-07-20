'''Main tests in API'''
import unittest
from test.stubs.repository import StubThematicRepository

class ThematicRepositoryPartitioningTest(unittest.TestCase):
    ''' Tests partitioning errors '''
    def test_default_partitioning_no_options(self):
        ''' Checks if the partition defined as MAIN is fetched when no option
            is given '''
        self.assertEqual(
            StubThematicRepository().get_default_partitioning(None),
            'cd_indicador'
        )

    def test_default_partitioning_no_theme(self):
        ''' Checks if the partition defined as MAIN is fetched when no partition
            is given in options '''
        self.assertEqual(
            StubThematicRepository().get_default_partitioning({}),
            'cd_indicador'
        )

    def test_default_partitioning_invalid_theme(self):
        ''' Checks if the partition defined as MAIN is fetched when an invalid
            theme is given in options '''
        self.assertEqual(
            StubThematicRepository().get_default_partitioning({"theme": "wrong"}),
            'cd_indicador'
        )

    def test_valid_theme_no_partition(self):
        ''' Checks if no partition is returned when the theme lists it in NONE '''
        self.assertEqual(
            StubThematicRepository().get_default_partitioning({"theme":"municipio"}),
            ''
        )
    
    def test_valid_theme(self):
        ''' Checks if the partition is returned correctly '''
        self.assertEqual(
            StubThematicRepository().get_default_partitioning({"theme":"provabrasil"}),
            'cd_tr_fora'
        )
