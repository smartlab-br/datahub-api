''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.sst.indicadores_br import IndicadoresSSTBrasilRepository

#pylint: disable=R0903
class IndicadoresSSTBrasil(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'SMARTLAB', 'link': 'http://smartlab.mpt.mp.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = IndicadoresSSTBrasilRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = IndicadoresSSTBrasilRepository()
        return self.repo
