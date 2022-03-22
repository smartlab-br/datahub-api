''' Gerenciamento de conexões com fontes de dados '''
from impala.dbapi import connect
import redis
from flask import g
from flask import current_app

def get_impala_connection():
    ''' Gerencia a conexão com o impala '''
    if not hasattr(g, 'impala_connection'):
        g.impala_connection = connect(
            host=current_app.config["IMPALA_HOST"],
            database='spai',
            port=int(current_app.config["IMPALA_PORT"]),
            kerberos_service_name="impala",
            auth_mechanism="GSSAPI",            
            use_ssl=True
        )
    return g.impala_connection

def get_redis_pool():
    ''' Gerencia a conexão com o redis '''
    if not hasattr(g, 'redis_pool'):
        g.redis_pool = redis.Redis(
            host=current_app.config['REDIS_HOST'],
            port=current_app.config['REDIS_PORT'], # 6379,
            db=current_app.config['REDIS_DB'] # 0
        )
    return g.redis_pool
