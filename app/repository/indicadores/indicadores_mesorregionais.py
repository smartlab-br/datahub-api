''' Repository para recuperar informações da CEE '''
from repository.base import HiveRepository

#pylint: disable=R0903
class IndicadoresMesorregionaisRepository(HiveRepository):
    ''' Definição do repo '''
    TABLE_NAMES = {
        'MAIN': 'indicadores_mesorregiao'
    }
    NAMED_QUERIES = {
        'QRY_FIND_DATASET': 'SELECT {} FROM {} {} {} {} {} {}',
    }
