''' Repository para recuperar informações de uma empresa '''
from repository.base import RedisRepository


#pylint: disable=R0903
class DatasetsRepository(RedisRepository):
    ''' Definição do repo '''
    REDIS_KEY = 'rx:ds'

    def retrieve(self):
        ''' Localiza o dicionário de datasources no REDIS '''
        return self.retrieve_hashset(self.REDIS_KEY)

    def store(self, datasets):
        ''' Inclui/atualiza dicionário de competências e datasources no REDIS '''
        self.get_dao().hmset(self.REDIS_KEY, datasets)
        return datasets
