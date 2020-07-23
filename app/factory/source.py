''' Class for instantiating query options builder objects '''
from model.source.base import BaseSource
from model.source.caged import BaseCaged, CagedSaldo
from model.source.aeronaves import Aeronaves
from model.source.auto import Auto
from model.source.catweb import Catweb
from model.source.rais import Rais
from model.source.renavam import Renavam
from model.source.sisben import Sisben
from model.source.rfb import BaseRfb, RfbSocios, RfbParticipacaoSocietaria

class SourceFactory():
    @staticmethod
    def create(df):
        if df == 'aeronaves':
            return Aeronaves()
        if df == 'auto':
            return Auto()
        if df == 'catweb':
            return Catweb()
        if df == 'rais':
            return Rais()
        if df == 'renavam':
            return Renavam()
        if df == 'sisben':
            return Sisben()
        # RFB
        if df == 'rfb':
            return BaseRfb()
        if df == 'rfbsocios':
            return RfbSocios()
        if df == 'rfbparticipacaosocietaria':
            return RfbParticipacaoSocietaria()
        # CAGED
        if df is not None and 'caged' in df:
            if df == 'cagedsaldo':
                return CagedSaldo()
            return BaseCaged()
        # Default
        return BaseSource()
