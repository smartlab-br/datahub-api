''' Controller para fornecer dados da CEE '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.base import BaseResource

class MigracoesEscravoResource(BaseResource):
    ''' Classe de múltiplas incidências '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: cd_municipio_ibge_nat, cd_municipio_ibge_res, \
            calc_idade_no_resgate, genero, grau_instrucao, raca_requerente, \
            ocupacao_cbo_pretendida2, ocupacao_cbo_atual2, subclasse_cnae_20, \
            nm_municipio_uf_nat, latitude_nat, longitude_nat, nm_uf_nat, \
            sg_uf_nat, cd_unidade_nat, cd_prt_nat, nm_prt_nat, nm_unidade_nat, \
            tp_unidade_nat, sg_unidade_nat, cd_mesorregiao_nat, \
            nm_mesorregiao_nat, cd_microrregiao_nat, nm_microrregiao_nat, \
            cd_regiao_nat, nm_regiao_nat, cd_municipio_ibge_dv_nat, \
            nm_municipio_nat, nm_municipio_sem_acento_nat, cd_uf_nat, \
            nm_municipio_uf_res, latitude_res, longitude_res, nm_uf_res, \
            sg_uf_res, cd_unidade_res, cd_prt_res, nm_prt_res, \
            nm_unidade_res, tp_unidade_res, sg_unidade_res, \
            cd_mesorregiao_res, nm_mesorregiao_res, cd_microrregiao_res, \
            nm_microrregiao_res, cd_regiao_res, nm_regiao_res, \
            cd_municipio_ibge_dv_res, nm_municipio_res, \
            nm_municipio_sem_acento_res e cd_uf_res. " + BaseResource.CAT_DETAIL}
    ]

    @swagger.doc({
        'tags':['migracoes'],
        'description':'Obtém todas as migracoes identificadas no resgate de um trbalhador.',
        'parameters': CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'Migracoes'}
        }
    })
    def get(self):
        ''' Obtém os registros de migracoes, conforme parâmetros informados '''
        options = self.build_options(request.args)
        options['theme'] = 'migracoesescravos'
        return self.__get_domain().find_dataset(options)
