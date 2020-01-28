''' Controller para fornecer dados da CEE '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.base import BaseResource

class BeneficiosResource(BaseResource):
    ''' Classe de múltiplos Benefícios '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: ano_beneficio, idade_beneficio, \
            cd_municipio_ibge_beneficio, cd_tp_sexo_empregado_beneficio, \
            cd_especie_beneficio, qt_despesa_total, qt_dias_perdidos, \
            cd_agrupamento_categoria_cid, cd_agrup_categoria_cid_agravo, \
            cd_agp_cat_cid_agrv_det_doenca, cd_categoria_cid_beneficio, \
            ds_categoria_cid_beneficio, ds_cbo2002, ds_cnae_classe, \
            cd_municipio_ibge_dv, cd_municipio_ibge, nm_municipio, \
            nm_municipio_sem_acento, cd_uf, latitude, longitude, nm_uf, \
            sg_uf, nm_municipio_uf, cd_unidade, cd_prt, nm_prt, \
            nm_unidade, tp_unidade, sg_unidade, cd_mesorregiao, \
            nm_mesorregiao, cd_microrregiao, nm_microrregiao, cd_regiao e \
            nm_regiao. \
            Para renomear campos do dataset de retorno, após o campo de \
            consulta, adicionar o novo nome, separado por '-' (ex: \
            campo-campo_novo)."}
    ]

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
        options['theme'] = 'sisben'
        return self.__get_domain().find_dataset(options)
