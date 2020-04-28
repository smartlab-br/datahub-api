''' Controller para fornecer dados da CEE '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.base import BaseResource

class CardTemplateResource(BaseResource):
    ''' Classe que obtém a estrutura de dados de um modelo de card. '''
    @swagger.doc({
        'tags':['card_template'],
        'description':'Obtém um a estrutura de dados de um modelo de card',
        'parameters':[
            {
                "name": "cd_template",
                "description": "Código do template",
                "required": True,
                "type": 'string',
                "in": "path"
            },
            {
                "name": "datasource",
                "description": "Identificação da fonte de dados",
                "required": True,
                "type": 'string',
                "in": "query"
            },
            {
                "name": "cd_indicador",
                "description": "Código do indicador",
                "required": True,
                "type": 'string',
                "in": "query"
            },
            {
                "name": "cd_analysis_unit",
                "description": "Id da unidade de análise",
                "required": True,
                "type": 'string',
                "in": "query"
            }
        ],
        'responses': {
            '200': {
                'description': 'Card'
            }
        }
    })
    def get(self, cd_template):
        ''' Obtém um a estrutura de dados de um modelo de card '''
        if 'datasource' in request.args:
            options = request.args.copy()
            options['theme'] = request.args.get('datasource')
            return self.get_domain().get_template(cd_template, options)
        raise ValueError('Datasource inválido ou sem templates')
