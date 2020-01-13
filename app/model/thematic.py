''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.thematic import ThematicRepository

#pylint: disable=R0903
class Thematic(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'MAIN': {'fonte': 'IBGE', 'link': 'http://ibge.gov.br/'},
        'SMARTLAB': [
            'sstindicadoresnacionais', 'sstindicadoresmunicipais',
            'sstindicadoresestaduais', 'sstindicadoresunidadempt',
            'tiindicadoresnacionais', 'tiindicadoresmunicipais', 
            'tiindicadoresestaduais', 'tiindicadoresunidadempt'
        ]

        'assistenciasocial': {'fonte': 'Censo SUAS(Sistema Único de Assistência social)', 'link': ''},

        'sisben': {'fonte': 'INSS - Instituto Nacional do Seguro Social', 'link': 'http://inss.gov.br/'},
        'catweb': {'fonte': 'Ministério da Economia - Secretaria de Trabalho', 'link': 'http://trabalho.gov.br/'},
        
        'mapear': {'fonte': 'PRF', 'link': 'https://www.prf.gov.br/'},
        'provabrasil': {'fonte': 'INEP, Prova Brasil', 'link': 'http://www.inep.gov.br/'},
        
        'censoagromunicipal': {'fonte': 'IBGE - Censo Agropecuário, Florestal e Aquícola, 2017', 'link': 'http://ibge.gov.br/'},
        'censoagroestadual': {'fonte': 'IBGE - Censo Agropecuário, Florestal e Aquícola, 2017', 'link': 'http://ibge.gov.br/'},
        'censoagronacional': {'fonte': 'IBGE - Censo Agropecuário, Florestal e Aquícola, 2017', 'link': 'http://ibge.gov.br/'},

        'incidenciaescravidao': {'fonte': 'Ministério da Economia - Secretaria de Trabalho', 'link': 'http://trabalho.gov.br/'},
        'migracoesescravos': {'fonte': 'Ministério da Economia - Secretaria de Trabalho', 'link': 'http://trabalho.gov.br/'},
        'operacoesresgate': {'fonte': 'Ministério da Economia - Secretaria de Trabalho', 'link': 'http://trabalho.gov.br/'},
        'teindicadoresnacionais': {'fonte': 'Ministério da Economia - Secretaria de Trabalho', 'link': 'http://trabalho.gov.br/'},
        'teindicadoresmunicipais': {'fonte': 'Ministério da Economia - Secretaria de Trabalho', 'link': 'http://trabalho.gov.br/'},
        'teindicadoresestaduais': {'fonte': 'Ministério da Economia - Secretaria de Trabalho', 'link': 'http://trabalho.gov.br/'},
        'teindicadoresunidadempt': {'fonte': 'Ministério da Economia - Secretaria de Trabalho', 'link': 'http://trabalho.gov.br/'},
        'temlexposicaoresgate': {'fonte': 'Ministério da Economia - Secretaria de Trabalho', 'link': 'http://trabalho.gov.br/'},
        'temlexposicaoresgatefeatures': {'fonte': 'Ministério da Economia - Secretaria de Trabalho', 'link': 'http://trabalho.gov.br/'},
        'temlexposicaonaturais': {'fonte': 'Ministério da Economia - Secretaria de Trabalho', 'link': 'http://trabalho.gov.br/'},
        'temlexposicaonaturaisfeatures': {'fonte': 'Ministério da Economia - Secretaria de Trabalho', 'link': 'http://trabalho.gov.br/'}
        
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = ThematicRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = ThematicRepository()
        return self.repo
    
    def fetch_metadata(self, options):
        if 'theme' not in options or options['theme'] not in self.DEFAULT_PARTITIONING:
            return self.METADATA['MAIN']
        return self.METADATA[options['theme']]

        if 'theme' not in options:
            return self.METADATA['MAIN']
        elif options['theme'] self.METADATA:
            return self.METADATA[options['theme']]
        elif options['theme'] self.METADATA['SMARTLAB']
            return {'fonte': 'SMARTLAB', 'link': 'http://smartlab.mpt.mp.br/'}
        return self.METADATA['MAIN']
