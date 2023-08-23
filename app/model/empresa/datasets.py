''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.empresa.datasets import DatasetsRepository
from model.thematic import Thematic
from flask import current_app


#pylint: disable=R0903
class Datasets(BaseModel):
    ''' Definição do repo '''

    def __init__(self):
        ''' Construtor '''
        self.repo = DatasetsRepository()
        self.DATASETS_COMPETENCIA = current_app.config["CONF_REPO_DATASETS_COMPETENCIA"]

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
        for key, value in self.DATASETS_COMPETENCIA.items():
            agregacao, coluna = value.split(" ")
            coluna_resultado = coluna
            options = {
                "categorias": [coluna],
                "agregacao": [agregacao],
                "ordenacao": [f"-{coluna}"],
                "theme": key
            }
            if agregacao == 'MAX':
                options['categorias'] = ['1']
                options['valor'] = [coluna]
                options.pop('ordenacao', None)
                coluna_resultado = f"agr_max_{coluna}"

            df = model.find_dataset(options)
            value_to_add = ",".join([str(item.get(coluna_resultado)).replace(".0", "") for item in df.get("dataset")])
            result[key] = value_to_add

            # Add ingestion date
            try:
                carga_df = model.find_dataset({
                    "categorias": ['1'],
                    "valor": ['dt_carga'],
                    "agregacao": ["MAX"],
                    "theme": key,
                    "no_wrap": True
                }).to_dict('records')
                if carga_df:
                    result[f"dt_carga_{key}"] = str(carga_df[0].get('agr_max_dt_carga'))
            except Exception as e:
                result[f"dt_carga_{key}"] = str(e)

        self.get_repo().store(result)
