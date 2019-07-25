''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.sst.indicadores_mun import IndicadoresSSTMunicipiosRepository

#pylint: disable=R0903
class IndicadoresSSTMunicipios(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'INSS', 'link': 'http://inss.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = IndicadoresSSTMunicipiosRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = IndicadoresSSTMunicipiosRepository()
        return self.repo
