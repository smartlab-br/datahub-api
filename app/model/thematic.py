''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.thematic import ThematicRepository

#pylint: disable=R0903
class Thematic(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'MAIN': {'fonte': 'IBGE', 'link': 'http://ibge.gov.br/'},
        'assistenciasocial': {'fonte': 'Censo SUAS(Sistema Único de Assistência social)', 'link': ''}
        'sisben': {'fonte': 'INSS - Instituto Nacional do Seguro Social', 'link': 'http://inss.gov.br/'},
        'catweb': {'fonte': 'Ministério da Economia - Secretaria de Trabalho', 'link': 'http://trabalho.gov.br/'},
        'sstindicadoresnacionais': {'fonte': 'SMARTLAB', 'link': 'http://smartlab.mpt.mp.br/'}, 
        'sstindicadoresmunicipais': {'fonte': 'SMARTLAB', 'link': 'http://smartlab.mpt.mp.br/'}, 
        'sstindicadoresestaduais': {'fonte': 'SMARTLAB', 'link': 'http://smartlab.mpt.mp.br/'}, 
        'sstindicadoresunidadempt': {'fonte': 'SMARTLAB', 'link': 'http://smartlab.mpt.mp.br/'},
        
        'incidenciaescravidao': 'incidencia_trabalho_escravo',
        'migracoesescravos': 'te_migracoes',
        'operacoesresgate': 'operacoes_trabalho_escravo'
        
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
