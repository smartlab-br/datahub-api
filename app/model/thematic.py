''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.thematic import ThematicRepository

#pylint: disable=R0903
class Thematic(BaseModel):
    ''' Definição do repo '''

    def __init__(self):
        ''' Construtor '''
        self.repo = None
        self.load_and_prepare()

    def load_and_prepare(self):
        self.repo = ThematicRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = ThematicRepository()
        return self.repo

    def fetch_metadata(self, options=None):
        ''' Gets the metadata from thematic datasets' definitions '''
        if options is not None and 'theme' in options:
            for _key, each_source in self.repo.METADATA.items():
                if options.get('theme') in each_source['datasets']:
                    return each_source['source']
        return self.repo.METADATA['ibge']['source']

    def get_column_defs(self, table_name):
        ''' Get the column name definitions, according to the table '''
        return self.get_repo().get_column_defs(table_name)

    def decode_column_defs(self, original, perspective):
        ''' Get the column name definitions, according to the table and the perspective '''
        return self.get_repo().decode_column_defs(original, perspective)

    def get_persp_values(self, theme, perspective=None):
        ''' Get the perspective values for a theme '''
        perspectives = self.get_repo().PERSP_VALUES.get(theme)
        if perspectives and perspective:
            tmp_perspectives = {
                k: v
                for
                k, v
                in
                perspectives.items()
                if
                k == perspective
            }
            if not bool(tmp_perspectives):
                raise AttributeError(f'Perspectiva inválida. Deve ser: {perspectives.keys()}')
            return tmp_perspectives
        return perspectives

    def get_persp_columns(self, theme):
        ''' Get the perspective values for a theme '''
        return self.get_repo().PERSP_COLUMNS.get(theme)
