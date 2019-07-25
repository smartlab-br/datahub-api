''' Repository para recuperar informações da CEE '''
from repository.base import ImpalaRepository

#pylint: disable=R0903
class OperacoesEscravoRepository(ImpalaRepository):
    ''' Definição do repo '''
    TABLE_NAMES = {
        'MAIN': 'operacoes_trabalho_escravo'
    }
    NAMED_QUERIES = {
        'QRY_FIND_DATASET': 'SELECT {} FROM {} {} {} {} {} {}'
    }
