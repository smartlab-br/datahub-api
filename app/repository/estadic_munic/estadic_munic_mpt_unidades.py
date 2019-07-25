''' Repository para recuperar informações da CEE '''
from repository.base import ImpalaRepository

#pylint: disable=R0903
class EstadicMunicMptUnidadesRepository(ImpalaRepository):
    ''' Definição do repo '''
    TABLE_NAMES = {
        'MAIN': 'estadic_munic_mpt_unidade'
    }
