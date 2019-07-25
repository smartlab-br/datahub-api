''' Controller para fornecer dados da CEE '''
from flask import request
from flask_restful_swagger_2 import swagger
from resources.base import BaseResource
from model.municipio import Municipio

class MunicipiosResource(BaseResource):
    ''' Classe de múltiplos Municípios '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: cd_municipio_ibge, cd_municipio_ibge_dv, \
            st_situacao, cd_municipio_sinpas, cd_municipio_siafi, \
            nm_municipio, nm_municipio_sem_acento, ds_observacao, \
            cd_municipio_sinonimos, cd_municipio_sinonimos_dv, \
            st_amazonia, st_fronteira, st_capital, cd_uf, ano_instalacao, \
            ano_extincao, cd_municipio_sucessor, latitude, longitude, \
            area, nm_uf, sg_uf, nm_municipio_uf, cd_unidade, cd_prt, \
            nm_prt, nm_unidade, tp_unidade, sg_unidade, cd_mesorregiao, \
            nm_mesorregiao, cd_microrregiao, nm_microrregiao, \
            nu_portaria_mpt, tp_area, cd_geomunicipio_ibge, \
            cd_municipio_rfb, cd_regiao e nm_regiao. \
            Para renomear campos do dataset de retorno, após o campo de \
            consulta, adicionar o novo nome, separado por '-' (ex: \
            campo-campo_novo)."}
    ]

    def __init__(self):
        ''' Construtor'''
        self.domain = Municipio()

    @swagger.doc({
        'tags':['municipio'],
        'description':'Obtém todos os Municípios, de acordo com os \
        parâmetros informados',
        'parameters': CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'Municípios'}
        }
    })
    def get(self):
        ''' Obtém os registros de Municípios, conforme parâmetros informados '''
        options = self.build_options(request.args)
        return self.__get_domain().find_dataset(options)

    def __get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = Municipio()
        return self.domain

class MunicipioResource(BaseResource):
    ''' Classe de Municipio '''
    def __init__(self):
        ''' Construtor'''
        self.domain = Municipio()

    @swagger.doc({
        'tags':['municipio'],
        'description':'Obtém um único município de acordo com o código do IBGE',
        'parameters':[
            {
                "name": "cd_municipio_ibge",
                "description": "Código do IBGE do município consultado",
                "required": False,
                "type": 'string',
                "in": "path"
            }
        ],
        'responses': {
            '200': {
                'description': 'Município'
            }
        }
    })
    def get(self, cd_municipio_ibge):
        ''' Obtém o registro de estabelecimento com um determinado cnpj '''
        return self.__get_domain().find_by_cd_ibge(cd_municipio_ibge).to_json(orient='records')

    def __get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = Municipio()
        return self.domain
