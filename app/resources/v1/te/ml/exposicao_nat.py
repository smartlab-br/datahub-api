''' Controller para fornecer dados da CEE '''
from flask import request
from flask_restful_swagger_2 import swagger
from resources.base import BaseResource
from model.thematic import Thematic

class MLExposicaoNaturalidadeResource(BaseResource):
    ''' Classe de múltiplas incidências '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: cd_mun_ibge, cd_mun_ibge_dv, vl_indicador, \
            nvl_indicador, fact, low_max, medium_max, high_max, cd_uf, \
            train_acc, validate_acc, train_fscore, validate_fscore, \
            train_fscore_label, validate_fscore_label, nm_municipio, \
            nm_municipio_uf, nm_uf, sg_uf, latitude, longitude, \
            altitude, cd_unidade, nm_unidade, tp_unidade, cd_prt, \
            nm_prt, cd_mesorregiao, nm_mesorregiao, cd_microrregiao, \
            nm_microrregiao, cd_regiao, nm_regiao. \
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
        options['theme'] = 'temlexposicaonaturais'
        return self.__get_domain().find_dataset(options)

    def __get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = Thematic()
        return self.domain
