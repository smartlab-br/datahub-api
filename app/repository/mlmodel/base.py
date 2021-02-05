""" Repository genérico """
import pickle
import requests
from flask import current_app


class MLModelsRepository():
    """ Conector para o repositório de modelos serializados """
    TIPO = 'classificacao'

    def get_model(self, model_id, algoritmo, versao='latest'):
        """ Gets a trained model """
        # Modelos treinados devem ser serializados com pickle e
        # receber a extensão .ml
        # Gets a template from git
        location = current_app.config['GIT_MLREPO_BASE_URL'].format(
            self.TIPO, algoritmo, model_id, versao
        )
        # Load and deserialize
        return pickle.loads(requests.get(location + '.ml', verify=False).content)

    def get_metadata(self, model_id, algoritmo, versao='latest'):
        """ Gets the score and other metadata of a trained model """
        # Performance de modelos treinados devem ser serializados com pickle e
        # receber a extensão .sc
        # Gets a template from git
        location = current_app.config['GIT_MLREPO_BASE_URL'].format(
            self.TIPO, algoritmo, model_id, versao
        )
        # Load and deserialize
        return pickle.loads(requests.get(location + '.sc', verify=False).content)
