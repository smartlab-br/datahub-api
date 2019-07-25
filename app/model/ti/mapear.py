''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.ti.mapear import MapearRepository

#pylint: disable=R0903
class MapearInfantil(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'PRF', 'link': 'https://www.prf.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = MapearRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = MapearRepository()
        return self.repo
