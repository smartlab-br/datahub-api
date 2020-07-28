''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.thematic import ThematicRepository

#pylint: disable=R0903
class Thematic(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'SMARTLAB': {
            'datasets': [
                'sstindicadoresnacionais', 'sstindicadoresmunicipais',
                'sstindicadoresestaduais', 'sstindicadoresunidadempt',
                'tiindicadoresnacionais', 'tiindicadoresmunicipais',
                'tiindicadoresestaduais', 'tiindicadoresunidadempt'
            ],
            'source': {
                'fonte': 'SMARTLAB',
                'link': 'https://smartlabbr.org/'
            }
        },
        'ibge': {
            'datasets': [],
            'source': {'fonte': 'IBGE', 'link': 'https://ibge.gov.br/'}
        },
        'ibge_censoagro': {
            'datasets': [
                'censoagromunicipal', 'censoagroestadual', 'censoagronacional'
            ],
            'source': {
                'fonte': 'IBGE - Censo Agropecuário, Florestal e Aquícola, 2017',
                'link': 'https://ibge.gov.br/'
            }
        },
        'trabalho': {
            'datasets': [
                'catweb', 'rais', 'cagedtrabalhador', 'caged',
                'cagedsaldo', 'cagedtrabalhadorano',
                'incidenciaescravidao', 'migracoesescravos',
                'operacoesresgate', 'teindicadoresnacionais',
                'teindicadoresmunicipais', 'teindicadoresestaduais',
                'teindicadoresunidadempt', 'temlexposicaoresgate',
                'temlexposicaoresgatefeatures', 'temlexposicaonaturais',
                'temlexposicaonaturaisfeatures'
            ],
            'source': {
                'fonte': 'Ministério da Economia - Secretaria de Trabalho',
                'link': 'http://trabalho.gov.br/'
            }
        },
        'denatran': {
            'datasets': ['renavam', 'aeronaves'],
            'source': {
                'fonte': 'Denatran',
                'link': 'https://infraestrutura.gov.br/denatran'
            }
        },
        'mpt': {
            'datasets': ['auto'],
            'source': {
                'fonte': 'MPT - Ministério Público do Trabalho',
                'link': 'https://mpt.mp.br'
            }
        },
        'rfb': {
            'datasets': ['rfb', 'rfbsocios', 'rfbparticipacaosocietaria'],
            'source': {
                'fonte': 'Receita Federal',
                'link': 'https://receita.economia.gov.br/'
            }
        },
        'assistenciasocial': {
            'datasets': ['assistenciasocial'],
            'source': {
                'fonte': 'Censo SUAS(Sistema Único de Assistência social)',
                'link': ''
            }
        },
        'seguridade': {
            'datasets': ['sisben'],
            'source': {
                'fonte': 'INSS - Instituto Nacional do Seguro Social',
                'link': 'https://inss.gov.br/'
            }
        },
        'prf': {
            'datasets': ['mapear'],
            'source': {'fonte': 'PRF', 'link': 'https://www.prf.gov.br/'},
        },
        'inep': {
            'datasets': ['provabrasil'],
            'source': {
                'fonte': 'INEP, Prova Brasil',
                'link': 'http://www.inep.gov.br/'
            }
        }
    }

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
            for _key, each_source in self.METADATA.items():
                if options.get('theme') in each_source['datasets']:
                    return each_source['source']
        return self.METADATA['ibge']['source']

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
