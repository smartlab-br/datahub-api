''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.estadic_munic.estadic_munic_uf import EstadicMunicUfRepository

from service.number_formatter import NumberFormatter

#pylint: disable=R0903
class EstadicMunicUf(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'IBGE', 'link': 'http://ibge.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = EstadicMunicUfRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = EstadicMunicUfRepository()
        return self.repo
