''' Controller para fornecer dados da CEE '''
from flask import request
from flask_restful_swagger_2 import swagger
from resources.base import BaseResource

class EstadicMunicResource(BaseResource):
    ''' Classe de múltiplos Indicadores de Presença do Estado nos Municípios '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: cd_indicador_spai, spai_status, spai_bin, \
            spai_ds, spai_ds_texto, ds_fonte, nu_ano_indicador, \
            vl_indicador, tema, sub_tema, cd_indicador, ds_indicador, \
            spai_vl_indicador, spai_vl_indicador_txt, total_br, \
            presenca_total_br, pct_presenca_br, cd_mun_ibge, cd_uf, \
            nm_uf, sg_uf, cd_regiao e nm_regiao. " + BaseResource.CAT_DETAIL}
    ]

    @swagger.doc({
        'tags':['estadic_munic'],
        'description':'Obtém todos os indicadores municipais, de acordo com os \
        parâmetros informados',
        'parameters': CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'Indicadores Municipais'}
        }
    })
    def get(self):
        ''' Obtém os registros de indicadores municipais, conforme parâmetros informados '''
        options = self.build_options(request.args)
        options['theme'] = 'estadicmunic'
        return self.get_domain().find_dataset(options)
