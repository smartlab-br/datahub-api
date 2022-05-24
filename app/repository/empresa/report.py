''' Repository para recuperar informações de uma empresa '''
import pika
from flask import current_app
from repository.base import RedisRepository

#pylint: disable=R0903
class ReportRepository(RedisRepository):
    ''' Definição do repo '''
    def find_report(self, key):
        ''' Localiza o report no REDIS '''
        return self.get_dao().get(key)

    def store(self, cnpj_raiz):
        ''' Inclui cnpj raiz na fila do RabbitMQ '''
        rabbitCredentials = pika.PlainCredentials(current_app.config["RABBIT_USER"], current_app.config["RABBIT_PASSWORD"])
        rabbitParameters = pika.ConnectionParameters(
            current_app.config["RABBIT_HOST"],
            current_app.config["RABBIT_PORT"],
            '/',
            rabbitCredentials
        )
        rabbitConn = pika.BlockingConnection(rabbitParameters)
        rabbitChannel = rabbitConn.channel()
        rabbitChannel.queue_declare(queue="polaris-compliance-input-report", durable=True)
        rabbitChannel.basic_publish(exchange='',
                            routing_key="polaris-compliance-input-report",
                            body=bytes(cnpj_raiz, 'utf-8'))
        rabbitConn.close()

    def store_status(self, key, value):
        ''' Store status in REDIS '''
        self.get_dao().set(key, value)

    def find_status(self, key):
        ''' Get status from REDIS '''
        return self.get_dao().get(key)

    def del_status(self, key):
        ''' Removes key from REDIS '''
        self.get_dao().delete(key)
