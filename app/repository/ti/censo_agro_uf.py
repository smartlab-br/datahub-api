''' Repository para recuperar informações da CEE '''
from repository.base import ImpalaRepository

#pylint: disable=R0903
class CensoAgroEstadosRepository(ImpalaRepository):
    ''' Definição do repo '''
    TABLE_NAMES = {
        'MAIN': 'censo_agro_uf'
    }
    DEFAULT_PARTITIONING = ''
