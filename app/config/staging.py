''' Config loader for production environment '''
import os
import json
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

    data, stat = zk.get("/spai/datahub-api/staging/conf_repo_thematic_table_names")
    CONF_REPO_THEMATIC = {"TABLE_NAMES": json.loads(data.decode("utf-8"))}
    data, stat = zk.get("/spai/datahub-api/staging/conf_repo_thematic_default_partitioning")
    CONF_REPO_THEMATIC['DEFAULT_PARTITIONING'] = json.loads(data.decode("utf-8"))
    data, stat = zk.get("/spai/datahub-api/staging/conf_repo_thematic_on_join")
    CONF_REPO_THEMATIC['ON_JOIN'] = json.loads(data.decode("utf-8"))
    data, stat = zk.get("/spai/datahub-api/staging/conf_repo_thematic_join_suffixes")
    CONF_REPO_THEMATIC['JOIN_SUFFIXES'] = json.loads(data.decode("utf-8"))

    data, stat = zk.get("/spai/datahub-api/staging/conf_repo_base_val_field")
    CONF_REPO_BASE = {"VAL_FIELD": data.decode("utf-8")}
    data, stat = zk.get("/spai/datahub-api/staging/conf_repo_base_default_grouping")
    CONF_REPO_BASE['DEFAULT_GROUPING'] = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/staging/conf_repo_base_default_partitioning")
    CONF_REPO_BASE['DEFAULT_PARTITIONING'] = data.decode("utf-8")
    data, stat = zk.get("/spai/datahub-api/staging/conf_repo_base_cnpj_raiz_columns")
    CONF_REPO_BASE['CNPJ_RAIZ_COLUMNS'] = json.loads(data.decode("utf-8"))
    data, stat = zk.get("/spai/datahub-api/staging/conf_repo_base_cnpj_columns")
    CONF_REPO_BASE['CNPJ_COLUMNS'] = json.loads(data.decode("utf-8"))
    data, stat = zk.get("/spai/datahub-api/staging/conf_repo_base_compet_columns")
    CONF_REPO_BASE['COMPET_COLUMNS'] = json.loads(data.decode("utf-8"))
    data, stat = zk.get("/spai/datahub-api/staging/conf_repo_base_pf_columns")
    CONF_REPO_BASE['PF_COLUMNS'] = json.loads(data.decode("utf-8"))
    data, stat = zk.get("/spai/datahub-api/staging/conf_repo_base_persp_columns")
    CONF_REPO_BASE['PERSP_COLUMNS'] = json.loads(data.decode("utf-8"))
    data, stat = zk.get("/spai/datahub-api/staging/conf_repo_base_on_join")
    CONF_REPO_BASE['ON_JOIN'] = json.loads(data.decode("utf-8"))
    data, stat = zk.get("/spai/datahub-api/staging/conf_repo_base_join_suffixes")
    CONF_REPO_BASE['JOIN_SUFFIXES'] = json.loads(data.decode("utf-8"))

    zk.stop()
    zk = None
    data = None
    stat = None
