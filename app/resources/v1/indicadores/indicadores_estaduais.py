''' Controller para fornecer dados da CEE '''
from flask import request
from flask_restful_swagger_2 import swagger
from resources.base import BaseResource
from model.indicadores.indicadores_estaduais import IndicadoresEstaduais

class IndicadoresEstaduaisResource(BaseResource):
    ''' Classe de múltiplos Indicadores Estaduais '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: cd_mun_ibge, cd_dimensao, \
            cd_divisao_territorial, cd_indicador, nm_indicador, \
            ds_indicador, ds_indicador_completo, ds_indicador_radical, \
            ds_indicador_prefixo, ds_indicador_curto, ds_agreg_primaria, \
            ds_agreg_secundaria, nu_competencia, nu_competencia_min, \
            nu_competencia_max, tp_competencia, ds_fonte, vl_indicador, \
            vl_indicador_br, rank_br, rank_br_total, media_br, \
            pct_br, vl_indicador_min_br, vl_indicador_max_br, \
            rank_uf_total, cd_uf, nm_uf, sg_uf, cd_regiao e nm_regiao. \
            Para renomear campos do dataset de retorno, após o campo de \
            consulta, adicionar o novo nome, separado por '-' (ex: \
            campo-campo_novo)."}
    ]

    def __init__(self):
        ''' Construtor'''
        self.domain = IndicadoresEstaduais()

    @swagger.doc({
        'tags':['indicadores_estaduais'],
        'description':'Obtém todos os indicadores estaduais, de acordo com os \
        parâmetros informados',
        'parameters': CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'Indicadores Estaduais'}
        }
    })
    def get(self):
        ''' Obtém os registros de indicadores estaduais, conforme parâmetros informados '''
        options = self.build_options(request.args)
        return self.__get_domain().find_dataset(options)

    def __get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = IndicadoresEstaduais()
        return self.domain
