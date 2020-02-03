''' Controller para fornecer dados da CEE '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.base import BaseResource

class CensoAgroEstadosResource(BaseResource):
    ''' Classe de múltiplas incidências '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: cd_uf, tot_ocupados, tot_ocup_men14, \
            perc_tot_14, men_14_parente, part_com_parentesco, \
            men_14_sem_parente e part_sem_parentesco. " + BaseResource.CAT_DETAIL}
    ]

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
        options['theme'] = 'censoagroestadual'
        return self.__get_domain().find_dataset(options)
