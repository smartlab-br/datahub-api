''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.sst.indicadores_uf import IndicadoresSSTEstadosRepository

#pylint: disable=R0903
class IndicadoresSSTEstados(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'INSS', 'link': 'http://inss.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = IndicadoresSSTEstadosRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = IndicadoresSSTEstadosRepository()
        return self.repo
