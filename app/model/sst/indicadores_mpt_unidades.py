''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.sst.indicadores_mpt_unidades import IndicadoresSSTMptUnidadesRepository

#pylint: disable=R0903
class IndicadoresSSTMptUnidades(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'IBGE', 'link': 'http://ibge.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = IndicadoresSSTMptUnidadesRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = IndicadoresSSTMptUnidadesRepository()
        return self.repo
