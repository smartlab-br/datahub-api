""" Model for getting report from mapbiomas and adding more data """
from model.base import BaseModel
from repository.mapbiomas.car import CarRepository
import requests
from datetime import datetime
import dateutil.relativedelta
from flask import current_app


class Car(BaseModel):
    """ Model for getting report from mapbiomas and adding more data """
    def __init__(self):
        """ Construtor """
        self.repo = CarRepository()

    def get_repo(self):
        """ Garantia de que o repo estará carregado """
        if self.repo is None:
            self.repo = CarRepository()
        return self.repo

    def find_by_alert_and_car(self, alert, car):
        """ Gather data from different sources and put them together """
        report = self.fetch_report_from_source(car, alert)
        if report is not None:
            report['mpt_data'] = self.get_repo().find_by_id(report.get('alertReport', {}).get('carCode'))
        return report

    def invoke_graphql_query(self, gql_qry, token=None):
        """ Abstraction to invoke graphql queries from MapBiomas """
        headers = {}
        if token is not None:
            headers["Authorization"] = f"""Bearer {token}"""
        resp = requests.post(
            current_app.config["MAPBIOMAS"].get('API_BASE_URL'),
            json={'query': gql_qry},
            headers=headers,
            verify=False
        )
        resp.raise_for_status()
        return resp

    def get_token(self):
        """ Get a token from MapBiomas """
        resp = self.invoke_graphql_query(
            f"""mutation {{
              createToken(
                email: "{current_app.config["MAPBIOMAS"].get('USER')}",
                password: "{current_app.config["MAPBIOMAS"].get('PASSWORD')}"
              )
              {{ token }}
            }}"""
        )
        return resp.json().get('data', {}).get('createToken', {}).get('token')

    def fetch_report_from_source(self, car, alert):
        """ Get report from MapBiomas """
        resp = self.invoke_graphql_query(
            f"""{{
                alertReport(alertId:{alert}, carId:{car}) {{
                    alertAreaInCar
                    carCode
                    images {{
                        alertInProperty
                        propertyInState
                    }}
                }}
            }}"""
        )
        return resp.json().get('data')

    def fetch_alerts_by_dates(self, timeframe, limit=50, offset=0):
        """ Get alerts from MapBiomas, given a timeframe """
        current_offset = offset
        result = []

        if 'publish_from' not in timeframe:
            timeframe['publish_from'] = datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
        else:
            timeframe['publish_from'] = datetime.fromtimestamp(timeframe.get('publish_from'))

        if 'publish_to' not in timeframe:
            timeframe['publish_to'] = datetime.now()
        else:
            timeframe['publish_to'] = datetime.fromtimestamp(timeframe.get('publish_to'))

        detect_from = ""
        detect_to = ""
        if 'detect_from' in timeframe:
            timeframe['detect_from'] = datetime.fromtimestamp(timeframe.get('detect_from'))
            detect_from = f'startDetectedAt: "{timeframe.get("detect_from").strftime("%d-%m-%Y %H:%M")}"'
            if 'detect_to' not in timeframe:
                timeframe['detect_to'] = datetime.now()
            else:
                timeframe['detect_to'] = datetime.fromtimestamp(timeframe.get('detect_to'))

        if 'detect_to' in timeframe:
            detect_to = detect_from = f'endDetectedAt: "{timeframe.get("detect_to").strftime("%d-%m-%Y %H:%M")}"'

        while len(result) < 50:
            # Show all alerts for a given time-frame
            resp = self.invoke_graphql_query(
                f"""{{
                    allPublishedAlerts(
                        startPublishedAt: "{timeframe.get('publish_from').strftime("%d-%m-%Y %H:%M")}" 
                        endPublishedAt: "{timeframe.get('publish_to').strftime("%d-%m-%Y %H:%M")}"
                        {detect_from}
                        {detect_to}
                        limit: {limit}
                        offset: {current_offset}
                    ) {{ cars {{ id }} id }}
                }}""",
                self.get_token()
            )
            # TODO - Filtrar por cpf/cnpj
            nu_alerts = resp.json().get('data', {}).get('allPublishedAlerts')
            result.extend(nu_alerts)
            if len(nu_alerts) < limit:
                break
            current_offset = offset + 1
        # f"""{{
        #     allPublishedAlerts(
        #         startPublishedAt: "11-05-2020 17:00"
        #         endPublishedAt: "31/05/2020 17h00"
        #         startDetectedAt: "11-05-2019"
        #         endDetectedAt: "2020/05/11",
        #         limit: {limit},
        #         offset: {offset}
        #     ) {{ cars {{ id }} id }}
        # }}""",
        return result
