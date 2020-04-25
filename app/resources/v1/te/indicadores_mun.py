''' Controller para fornecer dados da CEE '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.base import BaseResource

class IndicadoresEscravoMunicipiosResource(BaseResource):
    ''' Classe de múltiplas incidências '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": BaseResource.CAT_IND_MUN}
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
        options['theme'] = 'teindicadoresmunicipais'
        return self.get_domain().find_dataset(options)

#pylint: disable=W0221
class IndicadoresEscravoMunicipiosOpResource(IndicadoresEscravoMunicipiosResource):
    ''' Classe de múltiplas único município '''
    @swagger.doc({
        'tags': ['beneficio'],
        'description': 'Obtém todos os indicadores do trabalho escravo,'
                       'de acordo com a operação e os parâmetros informados.',
        'parameters': IndicadoresEscravoMunicipiosResource.CUSTOM_SWAGGER_PARAMS + \
            BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'Benefícios'}
        }
    })
    def get(self, operation):
        ''' Obtém os registros de Benefícios, conforme parâmetros informados '''
        options = self.build_options(request.args)
        options['theme'] = 'teindicadoresmunicipais'
        return self.get_domain().find_and_operate(operation, options)
