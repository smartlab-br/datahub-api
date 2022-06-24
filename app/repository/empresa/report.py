''' Repository para recuperar informações de uma empresa '''
import pika
from flask import current_app
from datasources import send_rabbit_message
from repository.base import RedisRepository

#pylint: disable=R0903
class ReportRepository(RedisRepository):
    ''' Definição do repo '''
    def find_report(self, key):
        ''' Localiza o report no REDIS '''
        return self.get_dao().get(key)

    def store(self, cnpj_raiz):
        ''' Inclui cnpj raiz na fila do RabbitMQ '''
        complianceQueue = "report"
        send_rabbit_message('compliance', complianceQueue, cnpj_raiz)

    def store_status(self, key, value):
        ''' Store status in REDIS '''
        self.get_dao().set(key, value)

    def find_status(self, key):
        ''' Get status from REDIS '''
        return self.get_dao().get(key)

    def del_status(self, key):
        ''' Removes key from REDIS '''
        self.get_dao().delete(key)
