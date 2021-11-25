""" Controller para incluir identificação no relatório do MapBiomas """
from flask_restful_swagger_2 import swagger
from resources.base import BaseResource
from model.mapbiomas.car import Car
from flask import request
from requests import HTTPError
from thriftpy2.transport.base import TTransportException
from pandas.io.sql import DatabaseError
from service.decorators.auth import authenticate

class MapbiomasAlertsResource(BaseResource):
    """ Classe de busca alertas do mapbiomas """
    def __init__(self):
        """ Construtor"""
        self.domain = Car()

    @swagger.doc({
        'tags': ['alerta'],
        'description': 'Laudo do mapbiomas com identificação do CAR',
        'parameters': [
            {"name": "cpfcnpj", "required": False, "type": 'string', "in": "query",
             "description": "CPF/CNPJ completo, com separadores, para filtro dos alertas/car."},
            {"name": "nome", "required": False, "type": 'string', "in": "query",
             "description": "Parte do nome (em bloco único) do proprietário para filtro dos alertas/car."},
            {"name": "nome_propriedade", "required": False, "type": 'string', "in": "query",
             "description": "Parte do nome (em bloco único) da propriedade para filtro dos alertas/car."},
            {"name": "siglauf", "required": False, "type": 'string', "in": "query",
             "description": "Lista de siglas de Unidade Federativa do alerta, separadas por vírgula."},
            {"name": "arearange", "required": False, "type": 'string', "in": "query",
             "description": "Area (ha) do alerta, mínimo e máximo, separados por vírgula."},
            {"name": "daterange", "required": False, "type": 'string', "in": "query",
             "description": "Data de identificação do alerta, início e fim separados por vírgula e formato YYYY-MM-DD."}
        ],
        'responses': {'200': {'description': 'Alertas'}}
    })
    @authenticate(
        domain="bifrost",
        event_tracker_options={
            "item": "laudo", "action": "search", "category": "mapbiomas", "additional_parameters": {"cpfcnpj": "query"}
        }
    )
    def get(self):
        """ Obtém conjunto de alertas para o período informado """
        try:
            return self.get_domain().filter_alerts(request.args.copy().to_dict(flat=False))
        except HTTPError:  # Falha ao obter dado do MapBiomas
            return {"origin": "Mapbiomas", "message": "Falha ao obter conjunto de alertas do mapbiomas"}, 500
        except (TTransportException, DatabaseError):
            return {"origin": "Smartlab", "message": "Falha ao obter dados identificados no datahub"}, 500

    def get_domain(self):
        """ Carrega o modelo de domínio, se não o encontrar """
        if self.domain is None:
            self.domain = Car()
        return self.domain

    def set_domain(self):
        """ Setter invoked from constructor """
        self.domain = Car()


class MapbiomasAlertResource(BaseResource):
    """ Classe de busca laudo do mapbiomas e injeção de identificação do CAR """
    def __init__(self):
        """ Construtor"""
        self.domain = Car()

    @swagger.doc({
        'tags': ['laudo'],
        'description': 'Laudo do mapbiomas com identificação do CAR',
        'parameters': [
            {"name": "alert_id", "required": True, "type": 'int', "in": "path",
             "description": "ID do alerta."},
            {"name": "car_id", "required": False, "type": 'int', "in": "query",
             "description": "ID do CAR para geração do laudo."},
            {"name": "car_code", "required": False, "type": 'string', "in": "query",
             "description": "Recibo do CAR para geração do laudo."}
        ],
        'responses': {'200': {'description': 'Laudo'}}
    })
    @authenticate(
        domain="bifrost",
        event_tracker_options={
            "item": "laudo", "action": "emit", "category": "mapbiomas",
            "additional_parameters": {"alert_id": "path", "car_id": "query", "car_code": "query"}
        }
    )
    def get(self, alert_id):
        """ Obtém conjunto de alertas para o período informado """
        try:
            data = self.get_domain().find_by_alert_and_car(alert_id, request.args.get('car_id'), request.args.get('car_code'))
            return data
        except HTTPError:  # Falha ao obter dado do MapBiomas
            return {"origin": "Mapbiomas", "message": "Falha ao obter alerta do mapbiomas"}, 500
        except (TTransportException, DatabaseError):
            return {"origin": "Smartlab", "message": "Falha ao obter dados identificados no datahub"}, 500
        except Exception as err:
            return {"origin": "Mapbiomas", "message": str(err)}, 500

    def get_domain(self):
        """ Carrega o modelo de domínio, se não o encontrar """
        if self.domain is None:
            self.domain = Car()
        return self.domain

    def set_domain(self):
        """ Setter invoked from constructor """
        self.domain = Car()

class MapbiomasAlertsFilterOptionsResource(BaseResource):
    """ Classe de busca alertas do mapbiomas """
    def __init__(self):
        """ Construtor"""
        self.domain = Car()

    @swagger.doc({
        'tags': ['alerta'],
        'description': 'Opções para filtros',
        'parameters': [],
        'responses': {'200': {'description': 'Opções de filtros'}}
    })
    @authenticate(
        domain="bifrost",
        event_tracker_options={
            "item": "filter_options", "action": "find", "category": "mapbiomas"
        }
    )
    def get(self):
        """ Obtém conjunto de alertas para o período informado """
        try:
            return self.get_domain().find_filters_options()
        except HTTPError:  # Falha ao obter dado do MapBiomas
            return {"origin": "Mapbiomas", "message": "Falha ao obter conjunto de alertas do mapbiomas"}, 500
        except (TTransportException, DatabaseError):
            return {"origin": "Smartlab", "message": "Falha ao obter dados identificados no datahub"}, 500

    def get_domain(self):
        """ Carrega o modelo de domínio, se não o encontrar """
        if self.domain is None:
            self.domain = Car()
        return self.domain

    def set_domain(self):
        """ Setter invoked from constructor """
        self.domain = Car()
