''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.te.ml.exposicao_nat import MLExposicaoNaturalidadeRepository

#pylint: disable=R0903
class MLExposicaoNaturalidade(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'Ministério da Economia - Secretaria de Trabalho', 'link': 'http://trabalho.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = MLExposicaoNaturalidadeRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = MLExposicaoNaturalidadeRepository()
        return self.repo
