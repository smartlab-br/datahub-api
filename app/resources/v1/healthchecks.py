""" Classes de health check """
import pika
from flask_restful import Resource
import requests
from flask import current_app
from datasources import get_impala_connection, get_redis_pool, test_hbase_connection, test_rabbit_connection


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
        result = {"impala": False, "hbase": False, "redis": False, "rabbit": False}
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
            result["hbase"] = test_hbase_connection()
        except:
            pass

        try:
            result["rabbit"] = test_rabbit_connection()
        except:
            pass
        return result
