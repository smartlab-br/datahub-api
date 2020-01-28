''' Controller para fornecer dados da CEE '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.base import BaseResource

class CatsResource(BaseResource):
    ''' Classe de múltiplos CAT '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: ds_agente_causador, dt_acidente, ds_cbo \
            ds_emitente_cat, hora_acidente, ds_natureza_lesao, \
            ds_parte_corpo_atingida, ds_tipo_acidente, \
            ds_tipo_local_acidente, cd_indica_obito, \
            st_dia_semana_acidente, ano_cat, cd_municipio_ibge_cat, \
            cd_numero_cat, idade_cat, cd_tipo_sexo_empregado_cat, \
            ds_cnae_classe_cat, st_acidente_feriado, \
            ds_grupo_agcausadores_cat, cd_municipio_ibge_dv, \
            cd_municipio_ibge, nm_municipio, nm_municipio_sem_acento, \
            cd_uf, latitude, longitude, nm_uf, sg_uf, nm_municipio_uf, \
            cd_unidade, cd_prt, nm_prt, nm_unidade, tp_unidade, \
            sg_unidade, cd_mesorregiao, nm_mesorregiao, cd_microrregiao, \
            nm_microrregiao, cd_regiao e nm_regiao. \
            Para renomear campos do dataset de retorno, após o campo de \
            consulta, adicionar o novo nome, separado por '-' (ex: \
            campo-campo_novo)."}
    ]

    @swagger.doc({
        'tags':['cat'],
        'description':'Obtém todas as CAT, de acordo com os parâmetros informados',
        'parameters': CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'CAT'}
        }
    })
    def get(self):
        ''' Obtém os registros de CAT, conforme parâmetros informados '''
        options = self.build_options(request.args)
        options['theme'] = 'catweb'
        return self.__get_domain().find_dataset(options)

class CatsOpResource(CatsResource):
    ''' Classe de múltiplas único município '''
    @swagger.doc({
        'tags': ['cat'],
        'description': 'Obtém todos os dados de CATs,'
                       'de acordo com a operação e os parâmetros informados.',
        'parameters': CatsResource.CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'CAT'}
        }
    })
    def get(self, operation):
        ''' Obtém os registros de CAT, conforme parâmetros informados '''
        options = self.build_options(request.args)
        options['theme'] = 'catweb'
        return self.__get_domain().find_and_operate(operation, options)
