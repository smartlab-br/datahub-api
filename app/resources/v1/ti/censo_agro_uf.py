''' Controller para fornecer dados da CEE '''
from flask import request
from flask_restful_swagger_2 import swagger
from resources.base import BaseResource
from model.ti.censo_agro_uf import CensoAgroEstados

class CensoAgroEstadosResource(BaseResource):
    ''' Classe de múltiplas incidências '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: cd_uf, tot_ocupados, tot_ocup_men14, \
            perc_tot_14, men_14_parente, part_com_parentesco, \
            men_14_sem_parente e part_sem_parentesco. \
            Para renomear campos do dataset de retorno, após o campo de \
            consulta, adicionar o novo nome, separado por '-' (ex: \
            campo-campo_novo)."}
    ]

    def __init__(self):
        ''' Construtor'''
        self.domain = CensoAgroEstados()

    @swagger.doc({
        'tags':['censo_agro'],
        'description':'Obtém todos os dados do censo de áreas rurais, de acordo \
            com os parâmetros informados.',
        'parameters': CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'Censo Agro'}
        }
    })
    def get(self):
        ''' Obtém os registros de Censo Rural, conforme parâmetros informados '''
        options = self.build_options(request.args)
        return self.__get_domain().find_dataset(options)

    def __get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = CensoAgroEstados()
        return self.domain
