''' Gerenciamento de conexões com fontes de dados '''
from impala.dbapi import connect
from flask import g
from flask import current_app

def get_impala_connection():
    ''' Gerencia a conexão com o impala '''
    if not hasattr(g, 'impala_connection'):
        g.impala_connection = connect(
            host=current_app.config["IMPALA_HOST"],
            database='spai',
            port=int(current_app.config["IMPALA_PORT"]),
            user=current_app.config["IMPALA_USER"],
            use_ssl=True
        )
    return g.impala_connection
