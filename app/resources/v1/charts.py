''' Controller para fornecer dados da CEE '''
from flask import request, Response
from flask_restful_swagger_2 import swagger
from resources.base import BaseResource
from model.chart import Chart

class ChartsResource(BaseResource):
    ''' Classe de múltiplos Indicadores Municipais '''
    def __init__(self):
        ''' Construtor'''
        self.domain = Chart()

    def get(self, chart_type):
        """ Obtém um gráfico a partir de um yaml identificado pelos parâmetros informados """
        options = request.args.copy()
        options = self.build_options(options, rules='charts')
        options['chart_type'] = chart_type
        content = self.__get_domain().get_chart(options)

        if options.get('as_image'):
            response = Response(content)
            response.headers.set('Content-Type', 'image/png')
            return response
        if content.get('mime'):
            return Response(content.get('div'), mimetype=content.get('mime'))
        return content

    def post(self):
        """ Obtém um gráfico a partir de um json de configuração passado no request body """
        options = request.get_json()
        options = self.build_options(options, rules='charts')
        content = self.__get_domain().get_chart(options)

        if options.get('as_image'):
            response = Response(content)
            response.headers.set('Content-Type', 'image/png')
            return response
        if content.get('mime'):
            return Response(content.get('div'), mimetype=content.get('mime'))
        return content

    def __get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = Chart()
        return self.domain
