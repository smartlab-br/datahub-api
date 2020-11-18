''' Controller para fornecer dados das organizações de assistência social '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.base import BaseResource
from model.empresa.empresa import Empresa

class EmpresaResource(BaseResource):
    ''' Classe de múltiplas incidências '''
    CUSTOM_SWAGGER_PARAMS = [
        {
            "name": "only_meta",
            "description": "Sinalizador que indica apenas o retorno dos metadados (S para sim)",
            "required": False,
            "type": 'string',
            "in": "query"
        }
    ]

    def __init__(self):
        ''' Construtor'''
        self.domain = None
        self.set_domain()

    @swagger.doc({
        'tags':['empresa'],
        'description':'Obtém todos os registros de uma única empresa',
        'parameters': BaseResource.EMPRESA_DEFAULT_SWAGGER_PARAMS + CUSTOM_SWAGGER_PARAMS,
        'responses': {
            '200': {
                'description': 'Todos os datasets da empresa'
            }
        }
    })
    def get(self, cnpj_raiz):
        ''' Obtém todos os datasets da empresa '''
        if self.is_invalid_id(cnpj_raiz):
            return 400, 'Cnpj raiz inválido (deve ter 8 caracteres exclusivamente numéricos)'
        options = request.args.copy()
        options['id_inv'] = cnpj_raiz
        options = self.build_person_options(options)

        try:
            result = self.get_domain().find_datasets(options)
            if 'invalid' in result:
                del result['invalid']
                return result, 202
            return result
        except TimeoutError as toe:
            print(toe)
            return "Não foi possível incluir a análise na fila. Tente novamente mais tarde", 504
        except (AttributeError, KeyError, ValueError) as err:
            return str(err), 400

    @swagger.doc({
        'tags':['empresa'],
        'description':'Insere uma empresa na fila de análises.',
        'parameters': [
            {
                "name": "cnpj_raiz",
                "description": "CNPJ Raiz da empresa consultada",
                "required": True,
                "type": 'string',
                "in": "path"
            },
            {
                "name": "dados", "required": False, "type": 'string', "in": "query",
                "description": "Tipo de dado que deve ser recarregado. "
            },
            {
                "name": "competencia", "required": False, "type": 'string', "in": "query",
                "description": "Competência que deve ser recarregada. "
            }
        ],
        'responses': {
            '201': {'description': 'Empresa'}
        }
    })
    def post(self, cnpj_raiz):
        ''' Requisita uma nova análise de uma empresa '''
        if self.is_invalid_id(cnpj_raiz):
            return 400, 'Cnpj raiz inválido (deve ter 8 caracteres exclusivamente numéricos)'
        try:
            self.get_domain().produce(cnpj_raiz, request.args.get('dados'), request.args.get('competencia'))
            return 'Análise em processamento', 201
        except TimeoutError as toe:
            print(toe)
            return "Não foi possível incluir a análise na fila. Tente novamente mais tarde", 504
        except (AttributeError, KeyError, ValueError) as err:
            return str(err), 400

    def get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.set_domain()
        return self.domain

    def set_domain(self):
        ''' Domain setter, called from constructor '''
        self.domain = Empresa()

    def is_invalid_id(self, cnpj_raiz):
        ''' Checks if the ID is valid '''
        if len(cnpj_raiz) != 8 or not cnpj_raiz.isdecimal():
            return True
        return False # Doesn't block if no error is found