''' Config loader for production environment '''
import os
from kazoo.client import KazooClient

#pylint: disable=R0903
class StagingConfig():
    ''' Config loader for production environment '''
    CORS_AUTOMATIC_OPTIONS = True

    zk = KazooClient(hosts=os.getenv('ZOOKEEPER_HOST') + ':' + os.getenv('ZOOKEEPER_PORT'))
    zk.start()

    data, stat = zk.get("/spai/datahub-api/staging/impala_host")
    IMPALA_HOST = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/staging/impala_port")
    IMPALA_PORT = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/staging/impala_user")
    IMPALA_USER = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/staging/impala_pwd")
    IMPALA_PWD = data.decode("utf-8")

    data, stat = zk.get("/spai/datahub-api/staging/git_viewconf_url")
    GIT_VIEWCONF_BASE_URL = data.decode("utf-8")

    data, stat = zk.get("/spai/datahub-api/staging/hbase_host")
    HBASE_HOST = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/staging/hbase_port")
    HBASE_PORT = data.decode("utf-8")

    data, stat = zk.get("/spai/datahub-api/staging/redis_host")
    REDIS_HOST = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/staging/redis_port")
    REDIS_PORT = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/staging/redis_db")
    REDIS_DB = data.decode("utf-8")
    # data, stat = zk.get("/spai/datahub-api/staging/redis_user")
    # REDIS_USER = data.decode("utf-8")
    # data, stat = zk.get("/spai/datahub-api/staging/redis_pwd")
    # REDIS_PWD = data.decode("utf-8")

    data, stat = zk.get("/spai/datahub-api/staging/kafka_host")
    KAFKA_HOST = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/staging/kafka_port")
    KAFKA_PORT = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/staging/kafka_schema")
    KAFKA_SCHEMA = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/staging/kafka_topic_prefix")
    KAFKA_TOPIC_PREFIX = data.decode("utf-8")

    zk.stop()
    zk = None
    data = None
    stat = None
