''' Controller para fornecer dados da CEE '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.base import BaseResource

class ThematicResource(BaseResource):
    ''' Classe de múltiplos Indicadores Municipais '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "theme", "required": False, "type": 'string', "in": "path",
         "description": "Identificador do tema para buscar a tabela \
            correspondente."},
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. " + BaseResource.CAT_DETAIL}
    ]

    @swagger.doc({
        'tags':['dataset'],
        'description':'Obtém todos os registros do dataset temático, de acordo \
            com os parâmetros informados',
        'parameters': CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'Dataset'}
        }
    })
    def get(self, theme):
        ''' Obtém os registros do dataset temático, conforme parâmetros informados '''
        options = self.build_options(request.args)
        options['theme'] = theme
        return self.get_domain().find_dataset(options)
