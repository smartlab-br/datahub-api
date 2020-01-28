''' Controller para fornecer dados da CEE '''
from flask_restful_swagger_2 import swagger
from flask import request
from resources.base import BaseResource
from model.thematic import Thematic

class ThematicResource(BaseResource):
    ''' Classe de múltiplos Indicadores Municipais '''
    def __init__(self):
        ''' Construtor'''
        self.domain = Thematic()

    @swagger.doc({
        'tags':['dataset'],
        'description':'Obtém todos os registros do dataset temático, de acordo \
            com os parâmetros informados',
        'parameters': [
            {"name": "theme", "required": False, "type": 'string', "in": "path",
             "description": "Identificador do tema para buscar a tabela \
                correspondente."},
            {"name": "categorias", "required": True, "type": 'string', "in": "query",
             "description": "Informações que devem ser trazidas no dataset. \
                Para renomear campos do dataset de retorno, após o campo de \
                consulta, adicionar o novo nome, separado por '-' (ex: \
                campo-campo_novo)."},
            {"name": "valor", "required": False, "type": 'string', "in": "query",
             "description": "Coluna com o valor agregado. Agrega o valor \
                presente na coluna informada (vide opções nas categorias), de \
                acordo com a função de agregação informada (vide parâmetro \
                agregacao)."},
            {"name": "agregacao", "required": False, "type": 'string', "in": "query",
             "description": "Função de agregação a ser usada. As funções \
                disponíveis são DISTINCT, COUNT, SUM, MAX, MIN, PCT_COUNT, \
                PCT_SUM, RANK_COUNT, RANK_SUM, RANK_DENSE_COUNT e \
                RANK_DESNE_SUM. \
                Os atributos retornados terão nome formado pelo nome da \
                função precedido de 'agr_' (ex. 'agr_sum')."},
            {"name": "ordenacao", "required": False, "type": 'string', "in": "query",
             "description": "Colunas de ordenação para o resultado, dentre \
                as colunas presentes nas categorias. Adicionalmente, pode-se \
                incluir a coluna de agregação (ex. 'sum'). Uma coluna com \
                ordenação inversa deve ser precedida de '-' \
                (ex. order=-sum)."},
            {"name": "filtros", "required": False, "type": 'string', "in": "query",
             "description": "Operações lógicas para a filtragem dos registros \
                do resultado. Operadores disponíveis: eq, ne, in, gt, ge, lt, le, \
                and e or. Como redigir: ',' para separar operações e '-' para \
                separar parâmetros da operação. \
                Exemplo: &filtros=ge-ano-2014,and,lt-ano-2018."},
            {"name": "calcs", "required": False, "type": 'string', "in": "query",
             "description": "Campo calculado sobre grupos padrões do resource. \
                Havendo qualquer agregação, o agrupamento será feito pelas \
                categorias fornecidas na query. \
                Calcs disponiveis: min_part, max_part, avg_part, var_part, \
                ln_var_part, norm_pos_part, ln_norm_pos_part, norm_part e \
                ln_norm_part."}
        ],
        'responses': {
            '200': {'description': 'Dataset'}
        }
    })
    def get(self, theme):
        ''' Obtém os registros do dataset temático, conforme parâmetros informados '''
        options = self.build_options(request.args)
        options['theme'] = theme
        return self.__get_domain().find_dataset(options)

    def __get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = Thematic()
        return self.domain
