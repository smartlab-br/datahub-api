''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.ti.indicadores_mun import IndicadoresTIMunicipiosRepository

#pylint: disable=R0903
class IndicadoresTIMunicipios(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'INSS', 'link': 'http://inss.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = IndicadoresTIMunicipiosRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = IndicadoresTIMunicipiosRepository()
        return self.repo
