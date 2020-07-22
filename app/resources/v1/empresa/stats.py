''' Controller para fornecer dados das organizações de assistência social '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.base import BaseResource
from model.empresa.empresa import Empresa

class EmpresaStatsResource(BaseResource):
    ''' Classe de múltiplas incidências '''
    DEFAULT_SWAGGER_PARAMS = [
        {
            "name": "dados",
            "description": "Fonte de dados para consulta (rais, caged, catweb etc)",
            "required": False,
            "type": 'string',
            "in": "query"
        },
        {
            "name": "competencia",
            "description": "Competência a ser retornada. Depende da fonte de dados \
                (ex. para uma fonte pode ser AAAA, enquanto para outras AAAAMM)",
            "required": False,
            "type": 'string',
            "in": "query"
        },
        {
            "name": "id_pf",
            "description": "Identificador da Pessoa Física, dentro da empresa. \
                Tem que informar o dataset (param 'dados')",
            "required": False,
            "type": 'string',
            "in": "query"
        },
        {
            "name": "reduzido",
            "description": "Sinalizador que indica conjunto reduzido de colunas (S para sim)",
            "required": False,
            "type": 'string',
            "in": "query"
        },
        {
            "name": "perspectiva",
            "description": "Valor que filtra uma perspectiva predefinida de um dataset \
                (ex. No catweb, 'Empregador'). Nem todos os datasets tem essa opção.",
            "required": False,
            "type": 'string',
            "in": "query"
        }
    ]
    CUSTOM_SWAGGER_PARAMS = [
        {
            "name": "cnpj_raiz", "required": True, "type": 'string', "in": "path",
            "description": "CNPJ Raiz da empresa consultada"
        }
    ]

    def __init__(self):
        ''' Construtor'''
        self.domain = None
        self.set_domain()

    @swagger.doc({
        'tags':['empresa'],
        'description':'Obtém estatísticas de uma única empresa',
        'parameters': DEFAULT_SWAGGER_PARAMS + CUSTOM_SWAGGER_PARAMS,
        'responses': {
            '200': {
                'description': 'Estatísticas da empresa'
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

        # try:
        result = self.get_domain().get_statistics(options)
        if 'invalid' in result:
            del result['invalid']
            return result, 202
        return result
        # except (AttributeError, KeyError, ValueError) as err:
        #     return str(err), 400

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