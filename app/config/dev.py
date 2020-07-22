''' Config loader for dev environment '''
import os

#pylint: disable=R0903
class DevelopmentConfig():
    ''' Config loader for dev environment '''
    IMPALA_HOST = os.getenv('IMPALA_HOST')
    IMPALA_PORT = os.getenv('IMPALA_PORT')
    IMPALA_USER = os.getenv('IMPALA_USER')
    IMPALA_PWD = os.getenv('IMPALA_PWD')

    GIT_VIEWCONF_BASE_URL = os.getenv('GIT_VIEWCONF_BASE_URL')

    HBASE_HOST = os.getenv('HBASE_HOST')
    HBASE_PORT = os.getenv('HBASE_PORT')

    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_DB = os.getenv('REDIS_DB')
    # REDIS_USER = os.getenv('REDIS_USER')
    # REDIS_PWD = os.getenv('REDIS_PWD')

    KAFKA_HOST = os.getenv('KAFKA_HOST')
    KAFKA_PORT = os.getenv('KAFKA_PORT')
    KAFKA_SCHEMA = os.getenv('KAFKA_SCHEMA')
    KAFKA_TOPIC_PREFIX = os.getenv('KAFKA_TOPIC_PREFIX')
