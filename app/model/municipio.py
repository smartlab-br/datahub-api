''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.municipio import MunicipioRepository

#pylint: disable=R0903
class Municipio(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'IBGE', 'link': 'https://ibge.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = MunicipioRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = MunicipioRepository()
        return self.repo

    def find_by_cd_ibge(self, cd_municipio_ibge):
        ''' Localiza um único município pelo código do IBGE '''
        return self.get_repo().find_by_cd_ibge(cd_municipio_ibge)
