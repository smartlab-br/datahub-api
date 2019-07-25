''' Gerenciamento de conexões com fontes de dados '''
from flask import g
from flask import current_app

def get_hive_connection():
    ''' Gerencia a conexão com o hive '''
    from pyhive import hive
    if not hasattr(g, 'hive_connection'):
        g.hive_connection = hive.connect(
            host=current_app.config['HIVE_HOST'],
            port=int(current_app.config['HIVE_PORT']),
            database='spai_druid',
            username=current_app.config['HIVE_USER']
        )
    return g.hive_connection

def get_impala_connection():
    ''' Gerencia a conexão com o impala '''
    from impala.dbapi import connect
    if not hasattr(g, 'impala_connection'):
        g.impala_connection = connect(
            host=current_app.config["IMPALA_HOST"],
            database='spai',
            port=int(current_app.config["IMPALA_PORT"]),
            user=current_app.config["IMPALA_USER"],
            use_ssl=True
        )
    return g.impala_connection
