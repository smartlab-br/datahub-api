''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.ti.indicadores_mpt_unidades import IndicadoresTIMptUnidadesRepository

#pylint: disable=R0903
class IndicadoresTIMptUnidades(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'IBGE', 'link': 'http://ibge.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = IndicadoresTIMptUnidadesRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = IndicadoresTIMptUnidadesRepository()
        return self.repo
