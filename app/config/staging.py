from kazoo.client import KazooClient
import os


class StagingConfig(object):

    zk = KazooClient(hosts=os.getenv('ZOOKEEPER_HOST') + ':' + os.getenv('ZOOKEEPER_PORT'))
    zk.start()
    data, stat = zk.get("/spai/datahub-api/staging/hive_host")
    HIVE_HOST = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/staging/hive_port")
    HIVE_PORT = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/staging/hive_user")
    HIVE_USER = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/staging/hive_pwd")
    HIVE_PWD = data.decode("utf-8")
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

    zk.stop()
    zk = None
    data = None
    stat = None
