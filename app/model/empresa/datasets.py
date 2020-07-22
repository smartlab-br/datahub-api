''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.empresa.datasets import DatasetsRepository

#pylint: disable=R0903
class Datasets(BaseModel):
    ''' Definição do repo '''

    def __init__(self):
        ''' Construtor '''
        self.repo = DatasetsRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = DatasetsRepository()
        return self.repo

    def retrieve(self):
        ''' Localiza o dicionário de datasources no REDIS '''
        return self.get_repo().retrieve()

    def generate(self):
        ''' Inclui/atualiza dicionário de competências e datasources no REDIS '''
        self.get_repo().store()
