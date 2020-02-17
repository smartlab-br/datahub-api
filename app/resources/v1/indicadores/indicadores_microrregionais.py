''' Controller para fornecer dados da CEE '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.base import BaseResource

class IndicadoresMicrorregionaisResource(BaseResource):
    ''' Classe de múltiplos Indicadores Microrregionais '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: cd_microrregiao, nm_microrregiao, \
            nm_indicador, ds_indicador, nu_ano_indicador, ds_fonte, \
            cd_dimensao, ds_grupo, ds_subgrupo, ds_operador e \
            vl_indicador. " + BaseResource.CAT_DETAIL}
    ]

    @swagger.doc({
        'tags':['indicadores_microrregionais'],
        'description':'Obtém todos os indicadores microrregionais, de acordo com os \
        parâmetros informados',
        'parameters': CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'Indicadores Microrregionais'}
        }
    })
    def get(self):
        ''' Obtém os registros de indicadores microrregionais, conforme parâmetros informados '''
        options = self.build_options(request.args)
        options['theme'] = 'indicadoresmicrorregionais'
        return self.get_domain().find_dataset(options)
