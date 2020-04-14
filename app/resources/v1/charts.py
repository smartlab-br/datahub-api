''' Controller para fornecer dados da CEE '''
from flask import request, Response
from flask_restful_swagger_2 import swagger
from resources.base import BaseResource
from model.chart import Chart

from flask import send_file

class ChartsResource(BaseResource):
    ''' Classe de múltiplos Indicadores Municipais '''
    def __init__(self):
        ''' Construtor'''
        self.domain = Chart()

    def get(self, chart_type):
        ''' Obtém os registros do dataset temático, conforme parâmetros informados '''
        options = request.args.copy()
        options = self.build_options(options, rules = 'charts')
        options['chart_type'] = chart_type
        content = self.__get_domain().get_chart(options)

        if options['as_image']:
            return send_file(content, attachment_filename="chart.png", mimetype="image/png")
        if content.get('mime'):
            return Response(content.get('div'), mimetype=content.get('mime'))
        return content

    def __get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = Chart()
        return self.domain