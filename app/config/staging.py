''' Config loader for production environment '''
import os
from kazoo.client import KazooClient

#pylint: disable=R0903
class StagingConfig():
    ''' Config loader for production environment '''
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

    zk.stop()
    zk = None
    data = None
    stat = None
