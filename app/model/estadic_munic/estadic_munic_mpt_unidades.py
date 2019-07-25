''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.estadic_munic.estadic_munic_mpt_unidades import EstadicMunicMptUnidadesRepository

#pylint: disable=R0903
class EstadicMunicMptUnidades(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'IBGE', 'link': 'http://ibge.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = EstadicMunicMptUnidadesRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = EstadicMunicMptUnidadesRepository()
        return self.repo
