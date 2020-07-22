''' Controller para fornecer dados das organizações de assistência social '''
import requests
from flask_restful_swagger_2 import swagger
from resources.base import BaseResource
from model.empresa.datasets import Datasets

class DatasetsResource(BaseResource):
    ''' Classe de múltiplas incidências '''
    def __init__(self):
        ''' Construtor'''
        self.domain = Datasets()

    @swagger.doc({
        'tags':['dataset'],
        'description':'Obtém todas as competências de datasources disponíveis',
        'responses': {
            '200': {
                'description': 'Todos os datasets e competências disponíveis'
            }
        }
    })
    def get(self):
        ''' Obtém todos os datasets e competências disponíveis '''
        try:
            return self.get_domain().retrieve()
        except requests.exceptions.HTTPError as error:
            # Whoops it wasn't a 200
            if error.response.status_code == 404:
                nfemsg = "Nenhuma análise feita ou última análise expirada. Solicite nova análise."
                return nfemsg, 404
            return "Error fetching data", error.response.status_code

    @swagger.doc({
        'tags':['dataset'],
        'description':'Grava o dicionário de datasets para consulta.',
        'responses': {
            '201': {'description': 'Datasets'}
        }
    })
    def post(self):
        ''' Regrava o dicionário padrão no REDIS '''
        try:
            return self.get_domain().generate(), 201
        except TimeoutError:
            return "Falha na gravação do dicionário", 504
        except (AttributeError, KeyError, ValueError) as err:
            return str(err), 500

    def get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = Datasets()
        return self.domain
