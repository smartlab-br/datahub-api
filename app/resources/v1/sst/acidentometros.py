""" Controller para fornecer dados da CEE """
from flask_restful_swagger_2 import swagger
from resources.base import BaseResource
from model.sst.acidentometros import AcidentometrosSST

class AcidentometrosSSTResource(BaseResource):
    """ Classe de múltiplas incidências """
    @swagger.doc({
        'tags': ['acidentometros'],
        'description': 'Obtém todos os dados dos acidentômetros.',
        'responses': {
            '200': {'description': 'Contadores'}
        }
    })
    def get(self):
        """ Obtém os dados dos acidentômetros """
        return self.get_domain().obter_acidentometros()

    def get_domain(self):
        """ Carrega o modelo de domínio, se não o encontrar """
        if self.domain is None:
            self.domain = AcidentometrosSST()
        return self.domain

    def set_domain(self):
        """ Setter invoked from constructor """
        self.domain = AcidentometrosSST()