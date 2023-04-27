''' Config loader for production environment '''
import os
import yaml

#pylint: disable=R0903
class ProductionConfig():
    ''' Config loader for production environment '''
    CORS_AUTOMATIC_OPTIONS = True

    api_context = os.getenv('API_CONTEXT')

    IMPALA_HOST = os.getenv('IMPALA_HOST')
    IMPALA_PORT = os.getenv('IMPALA_PORT')

    GIT_VIEWCONF_BASE_URL = os.getenv('GIT_VIEWCONF_BASE_URL')
    GIT_MLREPO_BASE_URL = os.getenv('GIT_MLREPO_BASE_URL')

    HBASE_HOST = os.getenv('HBASE_HOST')
    HBASE_PORT = os.getenv('HBASE_PORT')
    HBASE_DATABASE = os.getenv('HBASE_DATABASE')

    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_DB = os.getenv('REDIS_DB')
    
    RABBIT_HOST=os.getenv('RABBIT_HOST')
    RABBIT_PORT=os.getenv('RABBIT_PORT')
    RABBIT_USER=os.getenv('RABBIT_USER')
    RABBIT_PASSWORD=os.getenv('RABBIT_PASSWORD')
    RABBIT_ENV="prd"

    MAPBIOMAS = {
        "API_BASE_URL": os.getenv('MAPBIOMAS_API_BASE_URL'),
        "USER": os.getenv('MAPBIOMAS_USER'),
        "PASSWORD": os.getenv('MAPBIOMAS_PASSWORD')
    }

    CONF_REPO = yaml.safe_load(os.getenv("CONF_REPO"))
    CONF_REPO_METADATA = CONF_REPO.get("metadata", {})
    CONF_REPO_THEMATIC = {
        "TABLE_NAMES": CONF_REPO.get("thematic", {}).get("tableNames", {}),
        "DEFAULT_PARTITIONING": CONF_REPO.get("thematic", {}).get("defaultPartitioning", {}),
        "ON_JOIN": CONF_REPO.get("thematic", {}).get("onJoin", {}),
        "JOIN_SUFFIXES": CONF_REPO.get("thematic", {}).get("joinSuffixes", {}),
    }
    CONF_REPO_BASE = {
        "VAL_FIELD": CONF_REPO.get("base", {}).get("valField", {}),
        "DEFAULT_GROUPING": CONF_REPO.get("base", {}).get("defaultGrouping", {}),
        "DEFAULT_PARTITIONING": CONF_REPO.get("base", {}).get("defaultPartitioning", {}),
        "CNPJ_RAIZ_COLUMNS": CONF_REPO.get("base", {}).get("cnpjRaizColumns", {}),
        "CNPJ_COLUMNS": CONF_REPO.get("base", {}).get("cnpjColumns", {}),
        "COMPET_COLUMNS": CONF_REPO.get("base", {}).get("competColumns", {}),
        "PF_COLUMNS": CONF_REPO.get("base", {}).get("pfColumns", {}),
        "PERSP_COLUMNS": CONF_REPO.get("base", {}).get("perspColumns", {}),
        "PERSP_VALUES": CONF_REPO.get("base", {}).get("perspValues", {}),
        "ON_JOIN": CONF_REPO.get("base", {}).get("onJoin", {}),
        "JOIN_SUFFIXES": CONF_REPO.get("base", {}).get("joinSuffixes", {}),
    }

    AUTH_GATEWAYS = yaml.safe_load(os.getenv("AUTH_GATEWAYS"))
    EVENT_TRACKERS = yaml.safe_load(os.getenv("EVENT_TRACKERS"))
