''' Controller para fornecer dados da CEE '''
from flask_restful import Resource
from service.qry_options_builder import QueryOptionsBuilder
from model.thematic import Thematic

class BaseResource(Resource):
    ''' Classe de base de resource '''
    DEFAULT_SWAGGER_PARAMS = [
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
    ]

    @staticmethod
    def build_options(r_args):
        ''' Constrói as opções da pesquisa '''
        return QueryOptionsBuilder.build_options(r_args)

    def __init__(self):
        ''' Construtor'''
        self.domain = None
        self.__set_domain()

    def __get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = Thematic()
        return self.domain

    def __set_domain(self):
        ''' Setter invoked from constructor '''
        self.domain = Thematic()
