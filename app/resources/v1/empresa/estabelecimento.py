''' Controller para fornecer dados das organizações de assistência social '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.v1.empresa.empresa import EmpresaResource

#pylint: disable=W0221
class EstabelecimentoResource(EmpresaResource):
    ''' Classe de múltiplas incidências '''
    CUSTOM_SWAGGER_PARAMS = [
        {
            "name": "cnpj", "required": True, "type": 'string', "in": "path",
            "description": "CNPJ do estabelecimento consultado"
        }
    ]

    def __init__(self):
        ''' Construtor'''
        self.domain = None
        self.set_domain()

    @swagger.doc({
        'tags':['empresa'],
        'description':'Obtém todos os registros de um único estabelecimento',
        'parameters': CUSTOM_SWAGGER_PARAMS + EmpresaResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {
                'description': 'Todos os datasets do estabelecimento'
            }
        }
    })
    def get(self, cnpj):
        ''' Obtém todos os datasets da empresa '''
        if self.is_invalid_id(cnpj):
            return 400, 'Cnpj inválido (deve ter 14 caracteres exclusivamente numéricos)'
        options = request.args.copy()
        options['id_inv'] = cnpj
        options = self.build_person_options(options, mod='estabelecimento')

        try:
            result = self.get_domain().find_datasets(options)
            if 'invalid' in result:
                del result['invalid']
                return result, 202
            return result
        except TimeoutError as toe:
            print(toe)
            return "Não foi possível incluir a análise na fila. Tente novamente mais tarde", 504
        except (AttributeError, KeyError, ValueError) as err:
            return str(err), 400

    def is_invalid_id(self, cnpj):
        ''' Checks if the ID is valid '''
        if len(cnpj) != 14 or not cnpj.isdecimal():
            return True
        return False # Doesn't block if no error is found