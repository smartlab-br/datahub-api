''' Controller para fornecer dados da CEE '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.base import BaseResource

class IndicadoresEscravoMptUnidadesResource(BaseResource):
    ''' Classe de múltiplos Indicadores de Unidades do MPT '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: cd_mun_ibge, nu_competencia, \
            nu_competencia_min, nu_competencia_max, nm_uf, sg_uf, \
            cd_unidade, cd_prt, nm_prt, nm_unidade, tp_unidade, sg_unidade, \
            cd_mesorregiao, nm_mesorregiao, cd_microrregiao, nm_microrregiao, \
            cd_regiao, nm_regiao, cd_uf, cd_indicador, ds_agreg_primaria, \
            ds_agreg_secundaria, ds_indicador, vl_indicador, vl_indicador_prt, \
            vl_indicador_min_prt, vl_indicador_max_prt, media_prt, pct_prt, \
            rank_prt, rank_prt_total, vl_indicador_br, vl_indicador_min_br, \
            vl_indicador_max_br, media_br, pct_br, rank_br e \
            rank_br_total. " + BaseResource.CAT_DETAIL}
    ]

    @swagger.doc({
        'tags':['indicadores_mpt_regionais'],
        'description':'Obtém todos os indicadores de unidades do MPT, de \
        acordo com os parâmetros informados',
        'parameters': CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'Indicadores de Regionais do MPT'}
        }
    })
    def get(self):
        ''' Obtém os registros de indicadores regionais do MPT, conforme parâmetros informados '''
        options = self.build_options(request.args)
        options['theme'] = 'teindicadoresunidadempt'
        return self.get_domain().find_dataset(options)
