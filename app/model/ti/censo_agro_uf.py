''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.ti.censo_agro_uf import CensoAgroEstadosRepository

#pylint: disable=R0903
class CensoAgroEstados(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'IBGE - Censo Agropecuário, Florestal e Aquícola, 2017', 'link': 'http://ibge.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = CensoAgroEstadosRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = CensoAgroEstadosRepository()
        return self.repo
