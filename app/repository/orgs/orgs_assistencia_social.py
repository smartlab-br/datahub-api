''' Repository para recuperar órgãos de assistência social (CRAS e CREAS) '''
from repository.base import ImpalaRepository

#pylint: disable=R0903
class OrgsAssistenciaSocialRepository(ImpalaRepository):
    ''' Definição do repo '''
    TABLE_NAMES = {
        'MAIN': 'orgs_assistencia_social'
    }
    DEFAULT_PARTITIONING = ''
