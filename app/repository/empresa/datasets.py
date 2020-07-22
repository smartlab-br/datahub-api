''' Repository para recuperar informações de uma empresa '''
from repository.base import RedisRepository

#pylint: disable=R0903
class DatasetsRepository(RedisRepository):
    ''' Definição do repo '''
    REDIS_KEY = 'rx:ds'
    DATASETS = {
        'rais': '2017',
        'rfb': '2018',
        'sisben': '2018',
        'catweb': ','.join([str(ano) for ano in range(2018,2010, -1)]),
        'auto': ','.join([str(ano) for ano in range(2019,2001, -1)]),
        'caged': ','.join(['{:d}{:02d}'.format(ano,mes) for ano in range(2019,2008, -1) for mes in range(12, 0, -1) if not (ano == 2019 and mes > 9)]),
        'cagedsaldo': ','.join(['{:d}{:02d}'.format(ano,mes) for ano in range(2019,2008, -1) for mes in range(12, 0, -1) if not (ano == 2019 and mes > 9)]),
        'cagedtrabalhador': ','.join(['{:d}{:02d}'.format(ano,mes) for ano in range(2019,2002, -1) for mes in range(12, 0, -1) if not (ano == 2019 and mes > 9)]),
        'cagedtrabalhadorano': ','.join([str(ano) for ano in range(2019,2002, -1)]),
        'rfbsocios': '2018',
        'rfbparticipacaosocietaria': '2018',
        'renavam': '2018',
        'aeronaves': '2018'
    }

    def retrieve(self):
        ''' Localiza o dicionário de datasources no REDIS '''
        return self.retrieve_hashset(self.REDIS_KEY)

    def store(self):
        ''' Inclui/atualiza dicionário de competências e datasources no REDIS '''
        self.get_dao().hmset(self.REDIS_KEY, self.DATASETS)
        return self.DATASETS
