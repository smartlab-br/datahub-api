""" Repository para classificar e adicionar metadados ao retorno """
import pandas as pd
from repository.mlmodel.supervisionado.classificacao import ClassificacaoRepository


# pylint: disable=R0903
class Classificacao():
    """ Definição do repo """
    def __init__(self):
        """ Construtor """
        self.repo = ClassificacaoRepository()

    def get_repo(self):
        """ Garantia de que o repo estará carregado """
        if self.repo is None:
            self.repo = ClassificacaoRepository()
        return self.repo

    def classificar(self, model_id, dados, options):
        """ Classifica e adiciona os metadados """
        versao = 'latest'
        if 'versao' in options:
            versao = options.get('versao')
        model = self.get_repo().get_model(model_id, options.get('algoritmo'), versao)

        if 'proba' in options and options['proba'] == 'S':
            predictions = model.predict_proba(pd.DataFrame(dados)).tolist()
        else:
            predictions = model.predict(pd.DataFrame(dados)).tolist()

        return {
            'dataset': predictions,
            'metadata': self.get_repo().get_metadata(model_id, options.get('algoritmo'), versao)
        }
