''' Controller para fornecer dados da CEE '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.base import BaseResource
from model.thematic import Thematic

class IndicadoresEscravoBrasilResource(BaseResource):
    ''' Classe de múltiplas incidências '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: cd_mun_ibge, nu_competencia, \
            cd_indicador, ds_agreg_primaria, ds_agreg_secundaria, \
            ds_indicador, nu_competencia_min, nu_competencia_max, \
            vl_indicador, vl_indicador_min, vl_indicador_max e media_br. \
            Para renomear campos do dataset de retorno, após o campo de \
            consulta, adicionar o novo nome, separado por '-' (ex: \
            campo-campo_novo)."}
    ]

    def __init__(self):
        ''' Construtor'''
        self.domain = Thematic()

    @swagger.doc({
        'tags':['beneficio'],
        'description':'Obtém todos os benefícios do INSS, de acordo com os parâmetros informados.',
        'parameters': CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'Benefícios'}
        }
    })
    def get(self):
        ''' Obtém os registros de Benefícios, conforme parâmetros informados '''
        options = self.build_options(request.args)
        options['theme'] = 'teindicadoresnacionais'
        return self.__get_domain().find_dataset(options)

    def __get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = Thematic()
        return self.domain
