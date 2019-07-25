''' Controller para fornecer dados da CEE '''
from flask import request
from flask_restful_swagger_2 import swagger
from resources.base import BaseResource
from model.indicadores.indicadores_regionais import IndicadoresRegionais

class IndicadoresRegionaisResource(BaseResource):
    ''' Classe de múltiplos Indicadores Regionais '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: cd_regiao, nm_regiao, nm_indicador, \
            ds_indicador, nu_ano_indicador, ds_fonte, cd_dimensao, \
            ds_grupo, ds_subgrupo, ds_operador e vl_indicador. \
            Para renomear campos do dataset de retorno, após o campo de \
            consulta, adicionar o novo nome, separado por '-' (ex: \
            campo-campo_novo)."}
    ]

    def __init__(self):
        ''' Construtor'''
        self.domain = IndicadoresRegionais()

    @swagger.doc({
        'tags':['indicadores_regionais'],
        'description':'Obtém todos os indicadores regionais, de acordo com os \
        parâmetros informados',
        'parameters': CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'Indicadores Regionais'}
        }
    })
    def get(self):
        ''' Obtém os registros de indicadores regionais, conforme parâmetros informados '''
        options = self.build_options(request.args)
        return self.__get_domain().find_dataset(options)

    def __get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = IndicadoresRegionais()
        return self.domain
