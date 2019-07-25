''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.te.indicadores_mpt_unidades import IndicadoresEscravoMptUnidadesRepository

#pylint: disable=R0903
class IndicadoresEscravoMptUnidades(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'IBGE', 'link': 'http://ibge.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = IndicadoresEscravoMptUnidadesRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = IndicadoresEscravoMptUnidadesRepository()
        return self.repo
