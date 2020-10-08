''' Controller para fornecer dados da CEE '''
from flask import request
from flask_restful_swagger_2 import swagger
from resources.base import BaseResource

class CensoAgroMunicipiosResource(BaseResource):
    ''' Classe de múltiplas incidências '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: cod_mun, qt_ocupados, qt_ocupados_menores14, \
            percent_ocupados_men_14. " + BaseResource.CAT_DETAIL}
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
        options['theme'] = 'censoagromunicipal'
        return self.get_domain().find_dataset(options)
