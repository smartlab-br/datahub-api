""" Controller para fornecer respostas a classificações de modelos treinados """
from flask_restful_swagger_2 import swagger
from flask_restful import Resource
from flask import request
from model.mlmodel.supervisionado.classificacao import Classificacao


# pylint: disable=R0903
class ClassificacaoResource(Resource):
    """ Classe de resource de modelos de classificacao """
    def __init__(self):
        """ Construtor"""
        self.domain = Classificacao()

    @swagger.doc({
        'tags':['classe_predicao'],
        'description':'Obtém a classificação de um ou mais registros enviados no body',
        'parameters':[
            {
                "name": "model_id",
                "description": "ID do modelo treinado",
                "required": True,
                "type": 'string',
                "in": "path"
            },
            {
                "name": "algoritmo",
                "description": "Algoritmo usado no modelo",
                "required": False,
                "type": 'string',
                "in": "query"
            },
            {
                "name": "versao",
                "description": "Versão do modelo treinado",
                "required": False,
                "type": 'string',
                "in": "query"
            },
            {
                "name": "proba",
                "description": "Flag de que o resultado é probabilístico",
                "required": False,
                "type": 'string',
                "in": "query"
            },
            {
                "name": "dados",
                "description": "Dados sujeitos à predição",
                "required": False,
                "in": "body",
                "schema": "DataModel"
            }
        ],
        'responses': {
            '200': {
                'description': 'Predição dos dados enviados e metadados de performance do modelo'
            }
        }
    })
    def get(self, model_id):
        """ Obtém o resultado do modelo """
        return self.get_domain().classificar(model_id, request.json, request.args)

    def get_domain(self):
        """ Carrega o modelo de domínio, se não o encontrar """
        if self.domain is None:
            self.domain = Classificacao()
        return self.domain
