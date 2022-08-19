''' Gerenciamento de conexões com fontes de dados '''
from impala.dbapi import connect
import redis
import pika
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
    hbase_service=f'HTTP/{current_app.config["HBASE_HOST"]}@MPT.INTRA'
    __, krb_context = kerberos.authGSSClientInit(hbase_service)
    kerberos.authGSSClientStep(krb_context, "")
    negotiate_details = kerberos.authGSSClientResponse(krb_context)
    headers = {'Authorization': 'Negotiate ' + negotiate_details,'Content-Type':'application/binary'}
    return headers

def get_hbase_data(table, key, column_family = "", column = ""):
    ssl._create_default_https_context = ssl._create_unverified_context
    http_client = THttpClient.THttpClient(f'https://{current_app.config["HBASE_HOST"]}:{current_app.config["HBASE_PORT"]}/')
    http_client.setCustomHeaders(headers=get_hbase_kerberos_auth())
    protocol = TBinaryProtocol.TBinaryProtocol(http_client)
    http_client.open()
    client = Hbase.Client(protocol)
    if column_family == "":
        result = client.getRow(table, key)
    else:
        if column == "":
            result = client.getRowWithColumns(table, key, [column_family])
        else:
            result = client.getRowWithColumns(table, key, [f'{column_family}:{column}'])
    http_client.close()
    return result

def get_redis_pool():
    ''' Gerencia a conexão com o redis '''
    if not hasattr(g, 'redis_pool'):
        g.redis_pool = redis.Redis(
            host=current_app.config['REDIS_HOST'],
            port=current_app.config['REDIS_PORT'], # 6379,
            db=current_app.config['REDIS_DB'] # 0
        )
    return g.redis_pool

def send_rabbit_message(service, queue, msg):
    rabbit_credentials = pika.PlainCredentials(current_app.config["RABBIT_USER"], current_app.config["RABBIT_PASSWORD"])
    rabbit_vHost = f'/{service}/{current_app.config["RABBIT_ENV"]}'
    rabbit_parameters = pika.ConnectionParameters(
        current_app.config["RABBIT_HOST"],
        current_app.config["RABBIT_PORT"],
        rabbit_vHost,
        rabbit_credentials
    )
    rabbit_conn = pika.BlockingConnection(rabbit_parameters)
    rabbitChannel = rabbit_conn.channel()
    rabbitChannel.queue_declare(queue=queue, durable=True)
    rabbitChannel.basic_publish(exchange='',
                        routing_key=queue,
                        body=msg)
    rabbit_conn.close()

def test_hbase_connection():
    ssl._create_default_https_context = ssl._create_unverified_context
    http_client = THttpClient.THttpClient(f'https://{current_app.config["HBASE_HOST"]}:{current_app.config["HBASE_PORT"]}/')
    try:
        http_client.setCustomHeaders(headers=get_hbase_kerberos_auth())
        protocol = TBinaryProtocol.TBinaryProtocol(http_client)
        http_client.open()
        Hbase.Client(protocol)
        http_client.close()
        return True
    except:
        return False

def test_rabbit_connection():
    try:
        rabbit_credentials = pika.PlainCredentials(current_app.config["RABBIT_USER"], current_app.config["RABBIT_PASSWORD"])
        rabbit_parameters = pika.ConnectionParameters(
            current_app.config["RABBIT_HOST"],
            current_app.config["RABBIT_PORT"],
            '/',
            rabbit_credentials
        )
        rabbit_conn = pika.BlockingConnection(rabbit_parameters)
        rabbit_conn.close()
        return True
    except:
        return False
