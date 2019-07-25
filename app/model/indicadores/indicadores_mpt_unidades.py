''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.indicadores.indicadores_mpt_unidades import IndicadoresMptUnidadesRepository

#pylint: disable=R0903
class IndicadoresMptUnidades(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'IBGE', 'link': 'http://ibge.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = IndicadoresMptUnidadesRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = IndicadoresMptUnidadesRepository()
        return self.repo
