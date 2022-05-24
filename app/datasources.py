''' Gerenciamento de conexões com fontes de dados '''
from impala.dbapi import connect
import redis
from flask import g
from flask import current_app
from thrift.transport import THttpClient
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
import ssl
import kerberos 

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

def get_hbase_kerberos_auth():
    # this is the hbase service principal of HTTP, check with
    hbaseService=f'HTTP/{current_app.config["HBASE_HOST"]}@MPT.INTRA'
    __, krb_context = kerberos.authGSSClientInit(hbaseService)
    kerberos.authGSSClientStep(krb_context, "")
    negotiate_details = kerberos.authGSSClientResponse(krb_context)
    headers = {'Authorization': 'Negotiate ' + negotiate_details,'Content-Type':'application/binary'}
    return headers

def get_hbase_connection():
    ''' Gerencia a conexão com o hbase '''
    if not hasattr(g, 'hbase_connection'):
        ssl._create_default_https_context = ssl._create_unverified_context

        #cert_file is copied from CDP, use “find” to get the location, scp to your app server.
        httpClient = THttpClient.THttpClient(f'https://{current_app.config["HBASE_HOST"]}:{current_app.config["HBASE_PORT"]}/')
        # if no ssl verification is required
        httpClient.setCustomHeaders(headers=get_hbase_kerberos_auth())
        protocol = TBinaryProtocol.TBinaryProtocol(httpClient)
        httpClient.open()
        g.hbase_connection = Hbase.Client(protocol)
    return g.hbase_connection

def get_redis_pool():
    ''' Gerencia a conexão com o redis '''
    if not hasattr(g, 'redis_pool'):
        g.redis_pool = redis.Redis(
            host=current_app.config['REDIS_HOST'],
            port=current_app.config['REDIS_PORT'], # 6379,
            db=current_app.config['REDIS_DB'] # 0
        )
    return g.redis_pool
