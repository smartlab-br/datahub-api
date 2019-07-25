from kazoo.client import KazooClient
import os


class ProductionConfig(object):

    zk = KazooClient(hosts=os.getenv('ZOOKEEPER_HOST') + ':' + os.getenv('ZOOKEEPER_PORT'))
    zk.start()
    data, stat = zk.get("/spai/datahub-api/prod/hive_host")
    HIVE_HOST = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/prod/hive_port")
    HIVE_PORT = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/prod/hive_user")
    HIVE_USER = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/prod/hive_pwd")
    HIVE_PWD = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/prod/impala_host")
    IMPALA_HOST = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/prod/impala_port")
    IMPALA_PORT = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/prod/impala_user")
    IMPALA_USER = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/prod/impala_pwd")
    IMPALA_PWD = data.decode("utf-8")

    data, stat = zk.get("/spai/datahub-api/prod/git_viewconf_url")
    GIT_VIEWCONF_BASE_URL = data.decode("utf-8")

    zk.stop()
    zk = None
    data = None
    stat = None
