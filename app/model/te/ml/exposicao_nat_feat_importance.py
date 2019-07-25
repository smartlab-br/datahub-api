''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.te.ml.exposicao_nat_feat_importance \
    import MLExposicaoNaturalidadeFeatureImportanceRepository

#pylint: disable=R0903
class MLExposicaoNaturalidadeFeatureImportance(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'Ministério da Economia - Secretaria de Trabalho', 'link': 'http://trabalho.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = MLExposicaoNaturalidadeFeatureImportanceRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = MLExposicaoNaturalidadeFeatureImportanceRepository()
        return self.repo
