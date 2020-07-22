''' Controller para fornecer dados das organizações de assistência social '''
from flask_restful_swagger_2 import swagger
from flask import Response
from resources.v1.empresa.empresa import EmpresaResource
from model.empresa.report import Report

class ReportResource(EmpresaResource):
    ''' Classe de múltiplas incidências '''
    def __init__(self):
        ''' Construtor'''
        self.domain = None
        self.set_domain()

    @swagger.doc({
        'tags':['report'],
        'description':'Obtém o report gerado no Compliance',
        'parameters': EmpresaResource.CUSTOM_SWAGGER_PARAMS,
        'responses': {
            '200': {
                'description': 'Report (base-64)'
            }
        }
    })
    def get(self, cnpj_raiz):
        ''' Obtém o report '''
        if self.is_invalid_id(cnpj_raiz):
            return 400, 'Cnpj raiz inválido (deve ter 8 caracteres exclusivamente numéricos)'
        content = self.get_domain().find_report(cnpj_raiz)
        rsp_code = {'FAILED': 202, 'PROCESSING': 204, 'NOTFOUND': 202, 'RENEWING': 202, 'UNLOCKING': 202}
        if isinstance(content, dict):
            return '', rsp_code[content['status']]
        return Response(content, mimetype='text/html')

    @swagger.doc({
        'tags':['report'],
        'description': 'Envia CNPJ RAIZ para a fila de processamento do report.',
        'parameters': EmpresaResource.CUSTOM_SWAGGER_PARAMS,
        'responses': {
            '201': {'description': 'Report'}
        }
    })
    def post(self, cnpj_raiz):
        ''' Envia para a fila do Kafka '''
        if self.is_invalid_id(cnpj_raiz):
            return 400, 'Cnpj raiz inválido (deve ter 8 caracteres exclusivamente numéricos)'
        # content = self.get_domain().find_report(cnpj_raiz)
        # rsp_code = {'FAILED': 201, 'PROCESSING': 204, 'NOTFOUND': 201, 'RENEWING': 201, 'UNLOCKING': 201}
        # if isinstance(content, dict):
        #     return '', rsp_code[content['status']]
        # return Response(content, mimetype='text/html')
        try:
            return self.get_domain().generate(cnpj_raiz), 201
        except TimeoutError:
            return "Falha na gravação do dicionário", 504
        except (AttributeError, KeyError, ValueError) as err:
            return str(err), 500

    def get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.set_domain()
        return self.domain

    def set_domain(self):
        ''' Domain setter, called from constructor '''
        self.domain = Report()
