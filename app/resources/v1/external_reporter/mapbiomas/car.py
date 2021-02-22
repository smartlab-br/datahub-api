""" Controller para incluir identificação no relatório do MapBiomas """
import requests
from flask_restful_swagger_2 import swagger
from resources.base import BaseResource
from model.mapbiomas.car import Car
from flask import Response

class MapbiomasCarResource(BaseResource):
    """ Classe de busca laudo do mapbiomas e injeção de identificação do CAR """
    def __init__(self):
        """ Construtor"""
        self.domain = Car()

    @swagger.doc({
        'tags': ['municipio'],
        'description': 'Laudo do mapbiomas com identificação do CAR',
        'parameters': [
            {
                "name": "car",
                "description": "CAR",
                "required": True,
                "type": 'string',
                "in": "path"
            }
        ],
        'responses': {'200': {'description': 'Laudo'}}
    })
    def get(self, car):
        """ Obtém o registro de estabelecimento com um determinado cnpj """
        return Response(self.get_domain().find_by_car(car), mimetype='text/html',
                        headers={"Access-Control-Allow-Origin": "*"})

    def get_domain(self):
        """ Carrega o modelo de domínio, se não o encontrar """
        if self.domain is None:
            self.domain = Car()
        return self.domain

    def set_domain(self):
        """ Setter invoked from constructor """
        self.domain = Car()
