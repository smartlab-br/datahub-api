""" Classes de health check """
import pika
from flask_restful import Resource
import requests
from flask import current_app
from datasources import get_impala_connection, get_redis_pool, get_hbase_connection


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
            if get_hbase_connection():
                result["hbase"] = True
        except:
            pass

        try:
            rabbitCredentials = pika.PlainCredentials(current_app.config["RABBIT_USER"], current_app.config["RABBIT_PASSWORD"])
            rabbitParameters = pika.ConnectionParameters(
                current_app.config["RABBIT_HOST"],
                current_app.config["RABBIT_PORT"],
                '/',
                rabbitCredentials
            )
            rabbitConn = pika.BlockingConnection(rabbitParameters)
            rabbitConn.close()
            result["rabbit"] = True
        except:
            pass
        return result
