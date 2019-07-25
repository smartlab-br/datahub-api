''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.te.operacoes import OperacoesEscravoRepository

#pylint: disable=R0903
class OperacoesEscravo(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'Ministério da Economia - Secretaria de Trabalho', 'link': 'http://trabalho.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = OperacoesEscravoRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = OperacoesEscravoRepository()
        return self.repo
