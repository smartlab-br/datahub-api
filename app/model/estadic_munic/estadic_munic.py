''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.estadic_munic.estadic_munic import EstadicMunicRepository

from service.number_formatter import NumberFormatter

#pylint: disable=R0903
class EstadicMunic(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'IBGE', 'link': 'http://ibge.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = EstadicMunicRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = EstadicMunicRepository()
        return self.repo
