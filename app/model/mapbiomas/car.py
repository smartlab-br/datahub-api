""" Model for getting report from mapbiomas and adding more data """
from model.base import BaseModel
from repository.mapbiomas.car import CarRepository, MapBiomasConnectorRepository
import requests
from datetime import datetime
import dateutil.relativedelta
from flask import current_app


class Car(BaseModel):
    """ Model for getting report from mapbiomas and adding more data """
    def __init__(self):
        """ Construtor """
        self.repo = CarRepository()
        self.token = None

    def get_repo(self):
        """ Garantia de que o repo estará carregado """
        if self.repo is None:
            self.repo = CarRepository()
        return self.repo

    def find_by_alert_and_car(self, alert, car, car_code):
        """ Gather data from different sources and put them together """
        report = self.fetch_report_from_source(alert)
        if report is not None:
            if car_code:
                report['mpt_data'] = {
                    "ownership": self.get_repo().find_by_id(car_code)
                }
            else:
                report['mpt_data'] = {
                    "ownership": self.get_repo().find_by_id(report.get('alertReport', {}).get('carCode'))
                }
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
        if resp.json().get("errors"):
            retry = any([err.get("extensions", {}).get("forbidden", False) for err in resp.json().get("errors")])
            if retry:
                return self.invoke_graphql_query(gql_qry, self.get_token())
        return resp

    def get_token(self):
        """ Get a token from MapBiomas """
        if self.token is None:
            self.token = MapBiomasConnectorRepository().get_token()
            if self.token is None:
                resp = self.invoke_graphql_query(
                    f"""mutation {{
                      signIn(
                        email: "{current_app.config["MAPBIOMAS"].get('USER')}",
                        password: "{current_app.config["MAPBIOMAS"].get('PASSWORD')}"
                      )
                      {{ token }}
                    }}"""
                )
                if resp.json() is None:
                    return self.get_token()
                self.token = resp.json().get('data', {}).get('signIn', {}).get('token')
        return self.token

    def fetch_report_from_source(self, alert):
        """ Get report from MapBiomas """
        resp = self.invoke_graphql_query(
            f"""{{
                alertReport(alertCode:{alert}) {{
                    alertAreaInCar
                    alertCode
                    alertGeomWkt
                    areaHa
                    carCode
                    changes {{
                        labels
                        layer
                        overYears {{
                            imageUrl
                            year
                        }}
                    }}
                    imageGridMeasurements {{
                        latitude {{
                            endCoordinate
                            startCoordinate
                        }}
                        longitude {{
                            endCoordinate
                            startCoordinate
                        }}
                    }}
                    images {{
                        after {{
                            acquiredAt
                            satellite
                            url
                        }}
                        alertInProperty
                        before {{
                            acquiredAt
                            satellite
                            url
                        }}
                        labels
                        propertyInState
                    }}
                    intersections {{
                        conservationUnits {{
                            area
                            count
                        }}
                        deforestmentsAuthorized {{
                            area
                            count
                        }}
                        forestManagements {{
                            area
                            count
                        }}
                        indigenousLands {{
                            area
                            count
                        }}
                        settlements {{
                            area
                            count
                        }}
                        withRuralProperty {{
                            embargoes {{
                                area
                                count
                            }}
                            legalReserves {{
                                area
                                count
                            }}
                            permanentProtected {{
                                area
                                count
                            }}
                            riverSources {{
                                area
                                count
                            }}
                        }}
                    }}
                    simplifiedPoints {{
                        imageUrl
                        table {{
                            number
                            x
                            y
                        }}
                    }}
                    source
                    territories {{
                        categoryName
                        id
                        name
                    }}
                    warnings
                }}
            }}""",
            self.get_token()
        )

        if resp.json().get('data', None) is not None:
            return resp.json().get('data')

        message = "Erro não identificado"
        if 'errors' in resp.json():
            message = " | ".join([x.get('message') for x in resp.json().get('errors')])
        raise Exception(message) from None

    def fetch_alerts_by_owner_id(self, cpfcnpj):
        """ Fetch alerts for a given CAR """
        result = []
        for car in self.get_repo().find_by_filters({"cpfcnpj": cpfcnpj}):
            resp = self.invoke_graphql_query(
                f"""{{
                    alertsFromCar(
                        carCode:"{car.get("carcode")}"
                    )
                }}"""
            )

            alerts = [{**car, **{"alertId": alert}} for alert in resp.json().get('data', {}).get('alertsFromCar')]
            result.extend(alerts)
        return result

    def fetch_alerts_by_car(self, car):
        """ Get alerts for a specific CAR """
        result = []
        for each_car in car:
            car_complete_list = self.get_repo().find_by_id(each_car)
            for car_complete in car_complete_list:
                resp = self.invoke_graphql_query(
                    f"""{{
                        alertsFromCar(
                            carCode:"{each_car}"
                        )
                    }}""",
                    self.get_token()
                )

                result.extend([{**car_complete, **alert, **{"alertId": alert.get("alert_code")}} for alert in resp.json().get('data', {}).get('alertsFromCar')])
        return result

    def filter_alerts(self, options):
        """ Filter alerts by owner ID or publication date """
        page = int(options.get("page", ["1"])[0])
        if "cpfcnpj" in options:
            if not any([x in options for x in ["arearange", "daterange", "siglauf"]]):
                return self.fetch_cars_by_owner_id(options.get("cpfcnpj"), page)
            return self.get_repo().find_by_filters(options, page)
        if "car" in options:
            # return self.fetch_alerts_by_car(options.get("car"))
            return self.get_repo().find_by_id(options.get("car"), page)
        # return self.fetch_alerts_by_dates(options)
        if options.get("siglauf") or options.get("daterange", [',']) != [','] or options.get("arearange", ['0,0']) != ['0,0']:
            return self.get_repo().find_by_filters(options, page)
        return self.get_repo().find_all(page)

    def find_filters_options(self):
        return self.get_repo().find_filters_options()

    def fetch_cars_by_owner_id(self, id, page):
        """ Gets a list of CAR according to owner ID """
        return self.get_repo().find_by_filters({"cpfcnpj": id}, page)

    def fetch_alerts_by_dates(self, options, limit=50, offset=0):
        """ Get alerts from MapBiomas, given a options """
        current_offset = offset
        remote_limit_multiplier = 2
        result = []

        if 'publish_from' not in options:
            options['publish_from'] = datetime.now() + dateutil.relativedelta.relativedelta(months=-3)
        else:
            options['publish_from'] = datetime.fromtimestamp(options.get('publish_from'))

        if 'publish_to' not in options:
            options['publish_to'] = datetime.now()
        else:
            options['publish_to'] = datetime.fromtimestamp(options.get('publish_to'))

        detect_from = ""
        detect_to = ""
        if 'detect_from' in options:
            options['detect_from'] = datetime.fromtimestamp(options.get('detect_from'))
            detect_from = f'startDetectedAt: "{options.get("detect_from").strftime("%d-%m-%Y %H:%M")}"'
            if 'detect_to' not in options:
                options['detect_to'] = datetime.now()
            else:
                options['detect_to'] = datetime.fromtimestamp(options.get('detect_to'))

        if 'detect_to' in options:
            detect_to = f'endDetectedAt: "{options.get("detect_to").strftime("%d-%m-%Y %H:%M")}"'

        while len(result) < 50:
            # Show all alerts for a given time-frame
            resp = self.invoke_graphql_query(
                f"""{{
                    publishedAlerts(
                        startPublishedAt: "{options.get('publish_from').strftime("%d-%m-%Y %H:%M")}" 
                        endPublishedAt: "{options.get('publish_to').strftime("%d-%m-%Y %H:%M")}"
                        {detect_from}
                        {detect_to}
                        limit: {limit * remote_limit_multiplier}
                        offset: {current_offset}
                    ) {{ alertCode
                         alertInsertedAt
                         areaHa
                         cars {{
                            id
                            carCode
                         }}
                         coordinates {{
                            latitude
                            longitude
                         }}
                         detectedAt
                         geometry {{
                            areaHa
                            id
                         }}
                         id
                         source
                         statusId
                         statusInsertedAt }}
                }}""",
                self.get_token()
            )
            nu_alerts = resp.json().get('data', {}).get('publishedAlerts')

            filtered_cars = self.get_repo().find_by_id_list(
                list(set([car.get("carCode") for alert in nu_alerts for car in alert.get("cars")]))
            )
            candidates = None
            if filtered_cars is not None:
                candidates = {candidate.get('carcode'): candidate for candidate in filtered_cars}

            for alert in nu_alerts:
                # Replace the cars with only the viable, according to filters
                for car in alert.get('cars'):
                    if car.get('carCode') in candidates.keys():
                        # Adds owner data
                        nu_alert = {
                            **alert.copy(),
                            **{"car_id": car.get("id"), "carCode": car.get("carCode")},
                            **candidates.get(car.get('carCode'))
                        }
                        del nu_alert["cars"]
                        result.append(nu_alert)

            if len(nu_alerts) < limit:
                break
            current_offset = current_offset + limit * remote_limit_multiplier
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
        if len(result) > 50:
            return result[:50]
        return result
