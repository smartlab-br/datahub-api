''' Class for instantiating query options builder objects '''
from model.source.base import BaseSource
from model.source.caged import BaseCaged, CagedSaldo
from model.source.aeronaves import Aeronaves
from model.source.auto import Auto
from model.source.catweb import Catweb
from model.source.rais import Rais
# from model.source.renavam import Renavam
from model.source.sisben import Sisben
from model.source.rfb import BaseRfb, RfbSocios, RfbParticipacaoSocietaria
# from model.source.embarcacoes import Embarcacoes

class SourceFactory():
    ''' Factory for instantiating specific models depending on the source
        of data '''
    @staticmethod
    def create(dataframe):
        ''' Instantiation method '''
        if dataframe == 'aeronaves':
            return Aeronaves()
        if dataframe == 'auto':
            return Auto()
        if dataframe in ['catweb', 'catweb_c']:
            return Catweb()
        if dataframe == 'rais':
            return Rais()
        # if dataframe == 'renavam':
        #     return Renavam()
        if dataframe in ['sisben', 'sisben_c']:
            return Sisben()
        # RFB
        if dataframe == 'rfb':
            return BaseRfb()
        if dataframe == 'rfbsocios':
            return RfbSocios()
        if dataframe == 'rfbparticipacaosocietaria':
            return RfbParticipacaoSocietaria()
        # CAGED
        if dataframe is not None and 'caged' in dataframe:
            if dataframe == 'cagedsaldo':
                return CagedSaldo()
            return BaseCaged()
        # if dataframe == 'embarcacoes':
        #     return Embarcacoes()
        # Default
        return BaseSource()
