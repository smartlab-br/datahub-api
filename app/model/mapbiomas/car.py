""" Model for getting report from mapbiomas and adding more data """
from model.thematic import Thematic
import requests


class Car(Thematic):
    """ Model for getting report from mapbiomas and adding more data """
    def find_by_car_and_alert(self, car, alert):
        """ Gather data from different sources and put them together """
        car = '271752'
        report = self.fetch_report_from_source(car, alert)
        # car_data = self.find_dataset({})

        return report

    def fetch_report_from_source(self, car, alert):
        """ Get the HTML report from MapBiomas """
        alert = 90340
        car = 3618853
        gql_qry = f"""alertReport(alertId:{alert}, carId:{car}) {{
                        alertAreaInCar
                        carCode
                        images {{
                          alertInProperty
                          propertyInState
                        }}
                      }}"""
        resp = requests.post(
            f"https://plataforma.alerta.mapbiomas.org/app/graphql",
            json={'query': gql_qry},
            verify=False
        )
        resp.raise_for_status()
        return resp
