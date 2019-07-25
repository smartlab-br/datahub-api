''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.te.ml.exposicao_rgt_feat_importance \
    import MLExposicaoResgateFeatureImportanceRepository

#pylint: disable=R0903
class MLExposicaoResgateFeatureImportance(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'Ministério da Economia - Secretaria de Trabalho', 'link': 'http://trabalho.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = MLExposicaoResgateFeatureImportanceRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = MLExposicaoResgateFeatureImportanceRepository()
        return self.repo
