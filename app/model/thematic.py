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
                'catweb', 'incidenciaescravidao', 'migracoesescravos',
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
        self.repo = ThematicRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = ThematicRepository()
        return self.repo

    def fetch_metadata(self, options=None):
        ''' Gets the metadata from thematic datasets' definitions '''
        if options is not None and 'theme' in options:
            for each_source in self.METADATA.items():
                if options['theme'] in each_source['dataset']:
                    return each_source['source']
        return self.METADATA['ibge']['source']
