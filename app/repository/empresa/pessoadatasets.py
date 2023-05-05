''' Repository para recuperar informações de uma empresa '''
from datetime import datetime
from repository.base import RedisRepository

#pylint: disable=R0903
class PessoaDatasetsRepository(RedisRepository):
    ''' Definição do repo '''
    REDIS_BASE = 'rx:{}:{}:{}'

    def retrieve(self, id_pfpj, dataframe, pfpj='pj'):
        ''' Obtém o hashset de status de carregamento dco REDIS '''
        return self.retrieve_hashset(self.REDIS_BASE.format(pfpj, id_pfpj, dataframe))

    def store_status(self, id_pfpj, dataframe, competencias, pfpj="pj"):
        ''' Armazena um registro de status enviado para o rabbit '''
        status_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dict_status = {cmp: f"INGESTING|{status_date}" for cmp in competencias}
        self.get_dao().hmset(self.REDIS_BASE.format(pfpj, id_pfpj, dataframe), dict_status)
