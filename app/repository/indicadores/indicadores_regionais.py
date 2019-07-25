''' Repository para recuperar informações da CEE '''
from repository.base import HiveRepository

#pylint: disable=R0903
class IndicadoresRegionaisRepository(HiveRepository):
    ''' Definição do repo '''
    TABLE_NAMES = {
        'MAIN': 'indicadores_regiao'
    }
    NAMED_QUERIES = {
        'QRY_FIND_DATASET': 'SELECT {} FROM {} {} {} {} {} {}'
    }
