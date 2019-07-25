import os


class DevelopmentConfig(object):

    HIVE_HOST = os.getenv('HIVE_HOST')
    HIVE_PORT = os.getenv('HIVE_PORT')
    HIVE_USER = os.getenv('HIVE_USER')
    HIVE_PWD = os.getenv('HIVE_PWD')
    IMPALA_HOST = os.getenv('IMPALA_HOST')
    IMPALA_PORT = os.getenv('IMPALA_PORT')
    IMPALA_USER = os.getenv('IMPALA_USER')
    IMPALA_PWD = os.getenv('IMPALA_PWD')
    GIT_VIEWCONF_BASE_URL = os.getenv('GIT_VIEWCONF_BASE_URL')
