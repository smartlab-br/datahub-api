''' Controller para fornecer dados da CEE '''
from flask import request
from flask_restful_swagger_2 import swagger
from resources.base import BaseResource
from model.thematic import Thematic

class IndicadoresMesorregionaisResource(BaseResource):
    ''' Classe de múltiplos Indicadores Mesorregionais '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: cd_mesorregiao, nm_mesorregiao, \
            nm_indicador, ds_indicador, nu_ano_indicador, ds_fonte, \
            cd_dimensao, ds_grupo, ds_subgrupo, ds_operador e \
            vl_indicador. \
            Para renomear campos do dataset de retorno, após o campo de \
            consulta, adicionar o novo nome, separado por '-' (ex: \
            campo-campo_novo)."}
    ]

    def __init__(self):
        ''' Construtor'''
        self.domain = Thematic()

    @swagger.doc({
        'tags':['indicadores_mesorregionais'],
        'description':'Obtém todos os indicadores mesorregionais, de acordo com os \
        parâmetros informados',
        'parameters': CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'Indicadores Mesorregionais'}
        }
    })
    def get(self):
        ''' Obtém os registros de indicadores mesorregionais, conforme parâmetros informados '''
        options = self.build_options(request.args)
        options['theme'] = 'indicadoresmesorregionais'
        return self.__get_domain().find_dataset(options)

    def __get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = Thematic()
        return self.domain
