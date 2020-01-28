''' Controller para fornecer dados da CEE '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.base import BaseResource
from model.thematic import Thematic

class MLExposicaoNaturalidadeFeatureImportanceResource(BaseResource):
    ''' Classe de múltiplas incidências '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: cd_indicador, ds_indicador, \
            ds_indicador_curto, importancia. \
            Para renomear campos do dataset de retorno, após o campo de \
            consulta, adicionar o novo nome, separado por '-' (ex: \
            campo-campo_novo)."}
    ]

    def __init__(self):
        ''' Construtor'''
        self.domain = Thematic()

    @swagger.doc({
        'tags':['beneficio'],
        'description':'Obtém a classificação de todos os municípios.',
        'parameters': CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'Benefícios'}
        }
    })
    def get(self):
        ''' Obtém a classificação de todos os municípios '''
        options = self.build_options(request.args)
        options['theme'] = 'temlexposicaonaturaisfeatures'
        return self.__get_domain().find_dataset(options)

    def __get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = Thematic()
        return self.domain
