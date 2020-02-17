''' Controller para fornecer dados das organizações de assistência social '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.base import BaseResource

class OrgsAssistenciaSocialResource(BaseResource):
    ''' Classe de múltiplas incidências '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: categoria, razaoSocial, nome, municipio, uf, \
            endereco, bairro, referencia, cep, responsavel, cnpj, email, \
            google_lat,google_lng. " + BaseResource.CAT_DETAIL}
    ]

    @swagger.doc({
        'tags':['orgs_assistencia_social'],
        'description':'Obtém todos os dados das organizações de assistência \
            social, de acordo com os parâmetros informados.',
        'parameters': CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'CRAS e CREAS'}
        }
    })
    def get(self):
        ''' Obtém os registros de CRAS e CREAS, conforme parâmetros informados '''
        options = self.build_options(request.args)
        options['theme'] = 'assistenciasocial'
        return self.get_domain().find_dataset(options)
