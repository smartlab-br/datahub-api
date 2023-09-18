''' Class for instantiating query options builder objects '''
from model.source.base import BaseSource
from model.source.caged import CagedSaldo

class SourceFactory():
    ''' Factory for instantiating specific models depending on the source
        of data '''
    @staticmethod
    def create(dataframe):
        ''' Instantiation method '''
        if dataframe == 'cagedsaldo':
            return CagedSaldo()
        # Default
        return BaseSource()
