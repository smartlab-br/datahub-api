''' Controller para fornecer dados da CEE '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.base import BaseResource
from model.thematic import Thematic

class IndicadoresSSTEstadosResource(BaseResource):
    ''' Classe de múltiplas incidências '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: cd_mun_ibge, nu_competencia, \
            nu_competencia_min, nu_competencia_max, nm_uf, sg_uf, \
            cd_prt, nm_prt, cd_regiao, nm_regiao, cd_uf, cd_indicador, \
            ds_agreg_primaria, ds_agreg_secundaria, ds_indicador, \
            ds_fonte, vl_indicador, vl_indicador_br, vl_indicador_min_br, \
            vl_indicador_max_br, media_br, pct_br, rank_br e \
            rank_br_total. \
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
        options['theme'] = 'sstindicadoresestaduais'
        return self.__get_domain().find_dataset(options)

    def __get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = Thematic()
        return self.domain
