'''Main tests in API'''
import unittest
import pandas as pd
from model.charts.maps.choropleth import Choropleth

class ChoroplethGetGeometryLocTest(unittest.TestCase):
    ''' Test behaviours linked to fetching or changing headers from YAML options '''
    def test_no_options(self):
        self.assertEqual(
            Choropleth().get_geometry_loc(None, '1111111'),
            f'{Choropleth().BASE_TOPOJSON_REPO}/uf/municipio/11_q1.json'
        )

    def test_empty_options(self):
        self.assertEqual(
            Choropleth().get_geometry_loc({}, '1111111'),
            f'{Choropleth().BASE_TOPOJSON_REPO}/uf/municipio/11_q1.json'
        )

    def test_no_analysis_unit(self):
        self.assertEqual(
            Choropleth().get_geometry_loc({}, None),
            f'{Choropleth().BASE_TOPOJSON_REPO}/uf_q1.json'
        )

    def test_default_state_municipality(self):
        self.assertEqual(
            Choropleth().get_geometry_loc({'visao': 'uf'}, '1111111'),
            f'{Choropleth().BASE_TOPOJSON_REPO}/uf/municipio/11_q1.json'
        )

    def test_default_state_municipality_quality_2(self):
        self.assertEqual(
            Choropleth().get_geometry_loc(
                {'visao': 'uf', 'chart_options': {'quality': 2}},
                '1111111'
            ),
            f'{Choropleth().BASE_TOPOJSON_REPO}/uf/municipio/11_q2.json'
        )

    def test_default_topology_uf(self):
        self.assertEqual(
            Choropleth().get_geometry_loc(
                {'chart_options': {'topology': 'uf'}},
                '11'
            ),
            f'{Choropleth().BASE_TOPOJSON_REPO}/uf_q1.json'
        )

    def test_same_vision_and_resolution(self):
        self.assertEqual(
            Choropleth().get_geometry_loc(
                {'visao': 'uf', 'chart_options': {'resolution': 'uf'}},
                '11'
            ),
            f'{Choropleth().BASE_TOPOJSON_REPO}/uf/11_q1.json'
        )

    def test_location(self):
        self.assertEqual(
            Choropleth().get_geometry_loc(
                {'visao': 'distrito', 'chart_options': {'resolution': 'subdistrito'}},
                '111111111'
            ),
            f'{Choropleth().BASE_TOPOJSON_REPO}/distrito/subdistrito/111111111_q1.json'
        )
    