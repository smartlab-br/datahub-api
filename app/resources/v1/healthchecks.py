""" Classes de health check """
from flask_restful import Resource
import requests
from flask import current_app
from kafka import KafkaProducer
from datasources import get_impala_connection, get_redis_pool


class HCAlive(Resource):
    """ Liveness probe class """
    @classmethod
    def get(cls):
        """ Liveness probe """
        return {'message': 'OK'}


class HCReady(Resource):
    """ Readiness probe class """
    @classmethod
    def get(cls):
        """ Readiness probe """
        probe_analysis = {**cls.probe_databases()}
        if all(probe_analysis.values()):
            return probe_analysis
        return probe_analysis, 406

    @staticmethod
    def probe_databases():
        """ Checks if databases are up """
        result = {"impala": False, "hbase": False, "redis": False, "kafka": False}
        try:
            if get_impala_connection():
                result["impala"] = True
        except:
            pass

        try:
            if get_redis_pool():
                result["redis"] = True
        except:
            pass

        try:
            url = "http://{}:{}/{}/{}".format(
                current_app.config["HBASE_HOST"],
                current_app.config["HBASE_PORT"],
                "empresa",
                "schema"
            )
            response = requests.get(url, headers={'Accept': 'application/json'})
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
            result["hbase"] = True
        except:
            pass

        try:
            kafka_server = f'{current_app.config["KAFKA_HOST"]}:{current_app.config["KAFKA_PORT"]}'
            producer = KafkaProducer(bootstrap_servers=[kafka_server])
            producer.close()
            result["kafka"] = True
        except:
            pass
        return result
