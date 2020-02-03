''' Controller para fornecer dados da CEE '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.base import BaseResource

class IndicadoresNacionaisResource(BaseResource):
    ''' Classe de múltiplos Indicadores Nacionais '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: cd_mun_ibge, cd_dimensao, \
            cd_divisao_territorial, cd_indicador, nm_indicador, \
            ds_indicador, ds_indicador_completo, ds_indicador_radical, \
            ds_indicador_prefixo, ds_indicador_curto, ds_agreg_primaria, \
            ds_agreg_secundaria, nu_competencia, nu_competencia_min, \
            nu_competencia_max, tp_competencia, ds_fonte, vl_indicador e \
            rank_br_total. " + BaseResource.CAT_DETAIL}
    ]

    @swagger.doc({
        'tags':['indicadores_nacionais'],
        'description':'Obtém todos os indicadores nacionais, de acordo com os \
        parâmetros informados',
        'parameters': CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'Indicadores Nacionais'}
        }
    })
    def get(self):
        ''' Obtém os registros de indicadores nacionais, conforme parâmetros informados '''
        options = self.build_options(request.args)
        options['theme'] = 'indicadoresnacionais'
        return self.__get_domain().find_dataset(options)
