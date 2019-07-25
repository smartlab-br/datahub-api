''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.ti.prova_brasil import ProvaBrasilRepository

#pylint: disable=R0903
class ProvaBrasilInfantil(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'INEP, Prova Brasil', 'link': 'http://www.inep.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = ProvaBrasilRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = ProvaBrasilRepository()
        return self.repo
