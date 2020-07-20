''' Stubs for model testing '''
from io import StringIO
from service.pandas_operator import PandasOperator

class StubPandasOperator(PandasOperator):
    ''' Fake service to test instance methods '''
    @classmethod
    def get_cut_pattern(cls, pattern_id):
        ''' Fakes patterns from GIT '''
        return {'bins': [0, 18, 60, 100], 'right': False, 'labels': ['a', 'b', 'c']}
