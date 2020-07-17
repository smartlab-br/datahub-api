''' Controller para fornecer dados da CEE '''
from flask import request
from flask_restful_swagger_2 import swagger
from resources.base import BaseResource

class MapearInfantilResource(BaseResource):
    ''' Classe de múltiplas incidências '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: ds_br, ds_area, spai_ds_classific, spai_ds_risco_nivel, spai_id_explo_sexual_infantil,  \
            spai_id_reg_traf_consumo_droga, spai_id_atua_conselho_tutelar, spai_id_prostituicao_adulto, \
            spai_id_crianca_adolec_local, spai_id_ponto_consumo_alcool, spai_id_aglom_estacio_veiculo, \
            spai_id_vigi_privada_ambie, spai_id_iluminacao_area, spai_ds_faixa_etaria, spai_ds_genero, \
            cd_municipio_ibge_dv, cd_municipio_ibge, nm_municipio, nm_municipio_sem_acento, cd_uf, \
            latitude, longitude, nm_uf, sg_uf, nm_municipio_uf, cd_unidade, cd_prt, nm_prt, nm_unidade, \
            tp_unidade, sg_unidade, cd_mesorregiao, nm_mesorregiao, cd_microrregiao, nm_microrregiao, \
            cd_regiao e nm_regiao " + BaseResource.CAT_DETAIL}
    ]

    @swagger.doc({
        'tags':['mapear'],
        'description':'Obtém todas as informações coletadas pela PRF no Projeto MAPEAR.',
        'parameters': CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'Mapear'}
        }
    })
    def get(self):
        ''' Obtém os registros do Mapear, conforme parâmetros informados '''
        options = self.build_options(request.args)
        options['theme'] = 'mapear'
        return self.get_domain().find_dataset(options)
