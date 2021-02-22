""" Model for getting report from mapbiomas and adding more data """
from model.thematic import Thematic
import requests


class Car(Thematic):
    """ Model for getting report from mapbiomas and adding more data """
    def find_by_car(self, car):
        """ Gather data from different sources and put them together """
        car = '271752'
        report = self.fetch_report_from_source(car) \
            .replace("/static/", "https://plataforma.alerta.mapbiomas.org/") \
            .replace("http://localhost:5000/site.webmanifest", "https://plataforma.alerta.mapbiomas.org/site.webmanifest")
        # car_data = self.find_dataset({})

        return report

    def fetch_report_from_source(self, car):
        """ Get the HTML report from MapBiomas """
        resp = requests.get(f"https://plataforma.alerta.mapbiomas.org/laudos/{car}", verify=False)
        resp.raise_for_status()
        return resp.text
