''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.sst.beneficio import BeneficioRepository

#pylint: disable=R0903
class Beneficio(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'INSS - Instituto Nacional do Seguro Social', 'link': 'http://inss.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = BeneficioRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = BeneficioRepository()
        return self.repo
