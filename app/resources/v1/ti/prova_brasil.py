''' Controller para fornecer dados da CEE '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.base import BaseResource
from model.thematic import Thematic

class ProvaBrasilInfantilResource(BaseResource):
    ''' Classe de múltiplas incidências '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: id_municipio_aluno, ds_serie, nu_ano_prova_brasil, ds_indicador, cd_tr_fora, ds_idade, \
            vl_indicador, cd_municipio_ibge_dv, cd_municipio_ibge, nm_municipio, nm_municipio_sem_acento, cd_uf, latitude, \
            longitude, nm_uf, sg_uf, nm_municipio_uf, cd_unidade, cd_prt, nm_prt, nm_unidade, tp_unidade, sg_unidade, \
            cd_mesorregiao, nm_mesorregiao, cd_microrregiao, nm_microrregiao, cd_regiao, nm_regiao \
            Para renomear campos do dataset de retorno, após o campo de \
            consulta, adicionar o novo nome, separado por '-' (ex: \
            campo-campo_novo)."}
    ]

    def __init__(self):
        ''' Construtor'''
        self.domain = Thematic()

    @swagger.doc({
        'tags':['mapear'],
        'description':'Obtém as informações dos estudantes que trabalham fora coletadas pelo INEP no diagnostico da prova Brasil.',
        'parameters': CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'Prova Brasil'}
        }
    })
    def get(self):
        ''' Obtém os registros do Mapear, conforme parâmetros informados '''
        options = self.build_options(request.args)
        options['theme'] = 'provabrasil'
        return self.__get_domain().find_dataset(options)

    def __get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = Thematic()
        return self.domain
