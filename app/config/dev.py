''' Config loader for dev environment '''
import os

class DevelopmentConfig():
    ''' Config loader for dev environment '''
    IMPALA_HOST = os.getenv('IMPALA_HOST')
    IMPALA_PORT = os.getenv('IMPALA_PORT')
    IMPALA_USER = os.getenv('IMPALA_USER')
    IMPALA_PWD = os.getenv('IMPALA_PWD')
    GIT_VIEWCONF_BASE_URL = os.getenv('GIT_VIEWCONF_BASE_URL')
