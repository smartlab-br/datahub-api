''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.ti.indicadores_br import IndicadoresTIBrasilRepository

#pylint: disable=R0903
class IndicadoresTIBrasil(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'SMARTLAB', 'link': 'http://smartlab.mpt.mp.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = IndicadoresTIBrasilRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = IndicadoresTIBrasilRepository()
        return self.repo
