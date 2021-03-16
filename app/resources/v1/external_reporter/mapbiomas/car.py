""" Controller para incluir identificação no relatório do MapBiomas """
from flask_restful_swagger_2 import swagger
from resources.base import BaseResource
from model.mapbiomas.car import Car
from flask import Response, request

class MapbiomasAlertsResource(BaseResource):
    """ Classe de busca alertas do mapbiomas """
    def __init__(self):
        """ Construtor"""
        self.domain = Car()

    @swagger.doc({
        'tags': ['alerta'],
        'description': 'Laudo do mapbiomas com identificação do CAR',
        'parameters': [
            {"name": "publish_from", "required": False, "type": 'int', "in": "query",
             "description": "Timestamp do início do filtro de publicação do alerta."},
            {"name": "publish_to", "required": False, "type": 'int', "in": "query",
             "description": "Timestamp do fim do filtro de publicação do alerta."},
            {"name": "detect_from", "required": False, "type": 'int', "in": "query",
             "description": "Timestamp do início do filtro de detecção do alerta."},
            {"name": "detect_to", "required": False, "type": 'int', "in": "query",
             "description": "Timestamp do fim do filtro de detecção do alerta."},
        ],
        'responses': {'200': {'description': 'Alertas'}}
    })
    def get(self):
        """ Obtém conjunto de alertas para o período informado """
        return self.get_domain().fetch_alerts_by_dates(request.args.copy().to_dict(flat=False))

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
            {"name": "car_id", "required": True, "type": 'int', "in": "query",
             "description": "ID do CAR para geração do laudo."}
        ],
        'responses': {'200': {'description': 'Laudo'}}
    })
    def get(self, alert_id):
        """ Obtém conjunto de alertas para o período informado """
        return self.get_domain().find_by_alert_and_car(alert_id, request.args.get('car_id'))

    def get_domain(self):
        """ Carrega o modelo de domínio, se não o encontrar """
        if self.domain is None:
            self.domain = Car()
        return self.domain

    def set_domain(self):
        """ Setter invoked from constructor """
        self.domain = Car()
