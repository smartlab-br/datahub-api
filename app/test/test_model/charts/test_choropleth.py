'''Main tests in API'''
import unittest
from model.charts.maps.choropleth import Choropleth

class ChoroplethGetGeometryLocTest():
# class ChoroplethGetGeometryLocTest(unittest.TestCase):
    ''' Test behaviours linked to fetching or changing headers from YAML options '''
    def test_no_options(self):
        ''' Tests if default state-municipalities (vision-res) is returned when
            no option is given '''
        self.assertEqual(
            Choropleth().get_geometry_loc(None, '1111111'),
            f'{Choropleth().BASE_TOPOJSON_REPO}/uf/municipio/11_q1.json'
        )

    def test_empty_options(self):
        ''' Tests if default state-municipalities (vision-res) is returned when
            an empty option is given '''
        self.assertEqual(
            Choropleth().get_geometry_loc({}, '1111111'),
            f'{Choropleth().BASE_TOPOJSON_REPO}/uf/municipio/11_q1.json'
        )

    def test_no_analysis_unit(self):
        ''' Tests if default br-states (vision-res) is returned when no
            analysis unit ID is given '''
        self.assertEqual(
            Choropleth().get_geometry_loc({}, None),
            f'{Choropleth().BASE_TOPOJSON_REPO}/uf_q1.json'
        )

    def test_default_state_municipality(self):
        ''' Tests if default state-municipalities is loaded when vision and ID are
            passed as expected '''
        self.assertEqual(
            Choropleth().get_geometry_loc({'visao': 'uf'}, '1111111'),
            f'{Choropleth().BASE_TOPOJSON_REPO}/uf/municipio/11_q1.json'
        )

    def test_default_state_municipality_quality_2(self):
        ''' Tests if quality level is set accordingly '''
        self.assertEqual(
            Choropleth().get_geometry_loc(
                {'visao': 'uf', 'chart_options': {'quality': 2}},
                '1111111'
            ),
            f'{Choropleth().BASE_TOPOJSON_REPO}/uf/municipio/11_q2.json'
        )

    def test_default_topology_uf(self):
        ''' Tests if default br-states (vision-res) is returned when a state ID
            is passed as the analysis unit and the topology is set to uf '''
        self.assertEqual(
            Choropleth().get_geometry_loc(
                {'chart_options': {'topology': 'uf'}},
                '11'
            ),
            f'{Choropleth().BASE_TOPOJSON_REPO}/uf_q1.json'
        )

    def test_same_vision_and_resolution(self):
        ''' Tests if the appropriate topology location is returned when the
            vision matches the resolution '''
        self.assertEqual(
            Choropleth().get_geometry_loc(
                {'visao': 'uf', 'chart_options': {'resolution': 'uf'}},
                '11'
            ),
            f'{Choropleth().BASE_TOPOJSON_REPO}/uf/11_q1.json'
        )

    def test_location(self):
        ''' Tests if appropriate location is returned when all options are set
            correctly '''
        self.assertEqual(
            Choropleth().get_geometry_loc(
                {'visao': 'distrito', 'chart_options': {'resolution': 'subdistrito'}},
                '111111111'
            ),
            f'{Choropleth().BASE_TOPOJSON_REPO}/distrito/subdistrito/111111111_q1.json'
        )
    