''' Config loader for dev environment '''
import os
import json

#pylint: disable=R0903
class DevelopmentConfig():
    ''' Config loader for dev environment '''
    IMPALA_HOST = os.getenv('IMPALA_HOST')
    IMPALA_PORT = os.getenv('IMPALA_PORT')

    GIT_VIEWCONF_BASE_URL = os.getenv('GIT_VIEWCONF_BASE_URL')
    GIT_MLREPO_BASE_URL = os.getenv('GIT_MLREPO_BASE_URL')

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

    CONF_REPO_THEMATIC = {
        "TABLE_NAMES": json.loads(os.getenv("CONF_REPO_THEMATIC_TABLE_NAMES")),
        "DEFAULT_PARTITIONING": json.loads(os.getenv("CONF_REPO_THEMATIC_DEFAULT_PARTITIONING")),
        "ON_JOIN": json.loads(os.getenv("CONF_REPO_THEMATIC_ON_JOIN")),
        "JOIN_SUFFIXES": json.loads(os.getenv("CONF_REPO_THEMATIC_JOIN_SUFFIXES"))
    }
    CONF_REPO_BASE = {
        "VAL_FIELD": os.getenv("CONF_REPO_BASE_VAL_FIELD"),
        "DEFAULT_GROUPING": os.getenv("CONF_REPO_BASE_DEFAULT_GROUPING"),
        "DEFAULT_PARTITIONING": os.getenv("CONF_REPO_BASE_DEFAULT_PARTITIONING"),
        "CNPJ_RAIZ_COLUMNS": json.loads(os.getenv("CONF_REPO_BASE_CNPJ_RAIZ_COLUMNS")),
        "CNPJ_COLUMNS": json.loads(os.getenv("CONF_REPO_BASE_CNPJ_COLUMNS")),
        "COMPET_COLUMNS": json.loads(os.getenv("CONF_REPO_BASE_COMPET_COLUMNS")),
        "PF_COLUMNS": json.loads(os.getenv("CONF_REPO_BASE_PF_COLUMNS")),
        "PERSP_COLUMNS": json.loads(os.getenv("CONF_REPO_BASE_PERSP_COLUMNS")),
        "ON_JOIN": json.loads(os.getenv("CONF_REPO_BASE_ON_JOIN")),
        "JOIN_SUFFIXES": json.loads(os.getenv("CONF_REPO_BASE_JOIN_SUFFIXES"))
    }

    MAPBIOMAS = {
        "API_BASE_URL": os.getenv('MAPBIOMAS_API_BASE_URL'),
        "USER": os.getenv('MAPBIOMAS_USER'),
        "PASSWORD": os.getenv('MAPBIOMAS_PASSWORD')
    }

    AUTH_GATEWAYS = json.loads(os.getenv("AUTH_GATEWAYS"))
    EVENT_TRACKERS = json.loads(os.getenv("EVENT_TRACKERS"))