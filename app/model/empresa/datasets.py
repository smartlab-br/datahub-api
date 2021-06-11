''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.empresa.datasets import DatasetsRepository
from model.thematic import Thematic


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
        model = Thematic()

        result = {}
        for key, value in self.get_repo().DATASETS_COMPETENCIA.items():
            value_to_add = "2021"
            if value != 'NA':
                options = {
                    "categorias": [value],
                    "agregacao": ['distinct'],
                    "ordenacao": [f"-{value}"],
                    "theme": key
                }

                df = model.find_dataset(options)
                value_to_add = ",".join([str(item.get("nu_ano_rais")) for item in df.get("dataset")])
            result[key] = value_to_add

        self.get_repo().store(result)
