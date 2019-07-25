''' Controller para fornecer dados da CEE '''
from flask import request
from flask_restful import Resource
from flask_restful_swagger_2 import swagger
from model.estadic_munic.estadic_munic_uf import EstadicMunicUf
from model.estadic_munic.estadic_munic import EstadicMunic
from model.indicadores.indicadores_municipais import IndicadoresMunicipais
from model.indicadores.indicadores_estaduais import IndicadoresEstaduais
from model.indicadores.indicadores_nacionais import IndicadoresNacionais

class CardTemplateResource(Resource):
    ''' Classe que obtém a estrutura de dados de um modelo de card. '''
    DATASOURCES = {
        "estadicuf": EstadicMunicUf,
        "estadicmunic": EstadicMunic,
        "indicadoresmunicipais": IndicadoresMunicipais,
        "indicadoresestaduais": IndicadoresEstaduais,
        "indicadoresnacionais": IndicadoresNacionais
    }

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
        if ('datasource' in request.args and
                request.args.get('datasource') in self.DATASOURCES):
            domain = self.DATASOURCES[request.args.get('datasource')]()
        else:
            raise ValueError('Datasource inválido ou sem templates')
        return domain.get_template(cd_template, request.args)
