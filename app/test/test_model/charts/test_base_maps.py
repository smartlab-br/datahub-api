'''Main tests in API'''
import unittest
from model.charts.maps.base import BaseMap

class BaseMapGetHeadersTest(unittest.TestCase):
    ''' Test behaviours linked to fetching or changing headers from YAML options '''
    BASE_DESCRIPTION = [
        {"id": "ignore", "items": [
            {"label": "lbl_ign1_1", "value": "val_ign1_1", "id": "id_ign1_1"},
            {"label": "lbl_ign1_2", "value": "val_ign1_2", "id": "id_ign1_2"}
        ]},
        {"id": "selectlayer", "items": [
            {"label": "lbl_ok_1", "value": "val_ok_1", "id": "id_ok_1"},
            {"label": "lbl_ok_2", "value": "val_ok_2", "id": "id_ok_2"}
        ]},
        {"id": "ignore2", "items": [
            {"label": "lbl_ign2_1", "value": "val_ign2_1", "id": "id_ign2_1"},
            {"label": "lbl_ign2_2", "value": "val_ign2_2", "id": "id_ign2_2"}
        ]}
    ]
    BASE_EXPECT = [
        {"text": "lbl_ok_1", "layer_id": "val_ok_1", "value": "id_ok_1"},
        {"text": "lbl_ok_2", "layer_id": "val_ok_2", "value": "id_ok_2"}
    ]

    def test_existing_headers_no_chart_options(self):
        ''' Tests if returns the existing headers AS-IS '''
        options = {'headers': {'name': 'test'}}
        self.assertEqual(
            BaseMap.get_headers(None, options),
            options
        )

    def test_existing_headers(self):
        ''' Tests if returns the existing headers AS-IS '''
        options = {'headers': {'name': 'test'}}
        self.assertEqual(
            BaseMap.get_headers({'name_field': 'au_field'}, options),
            options
        )

    def test_existing_headers_over_description(self):
        ''' Tests if headers prevails when there's also description option '''
        options = {'headers': {'name': 'test'}, 'description': self.BASE_DESCRIPTION}
        self.assertEqual(
            BaseMap.get_headers({'name_field': 'au_field'}, options),
            options
        )
    
    def test_existing_description_no_chart_options(self):
        ''' Tests if returns the expected result, with default 'nm_municipio' header
            when no chart_option is sent '''
        options = {'description': self.BASE_DESCRIPTION}
        self.assertEqual(
            BaseMap.get_headers(None, options),
            [{'text': 'Analysis Unit', 'value': 'nm_municipio'}].extend(self.BASE_EXPECT)
        )

    def test_existing_description(self):
        ''' Tests if returns the expected header build using card description options '''
        options = {'description': self.BASE_DESCRIPTION}
        self.assertEqual(
            BaseMap.get_headers({'name_field': 'au_field'}, options),
            [{'text': 'Analysis Unit', 'value': 'au_field'}].extend(self.BASE_EXPECT)
        )

    def test_existing_description_default_au_field(self):
        ''' Tests if returns the expected result, with default 'nm_municipio' header
            when there's no name_field attribute in chart_options '''
        options = {'description': self.BASE_DESCRIPTION}
        self.assertEqual(
            BaseMap.get_headers({}, options),
            [{'text': 'Analysis Unit', 'value': 'nm_municipio'}].extend(self.BASE_EXPECT)
        )


    # @staticmethod
    # def get_location_columns(chart_options):
    #     ''' Get the column names to use as reference to location and value in the dataframe '''
    #     cols = [chart_options.get('lat', 'lat'), chart_options.get('long', 'long')]
    #     if 'value_field' in chart_options:
    #         cols.append(chart_options.get('value_field'))
    #     return cols
    # @staticmethod
    # def prepare_dataframe(dataframe, chart_options):
    #     ''' Creates a standard index for the dataframes '''
    #     dataframe['str_id'] = dataframe[chart_options.get('id_field', 'cd_mun_ibge')].astype(str)
    #     dataframe['idx'] = dataframe[chart_options.get('id_field', 'cd_mun_ibge')]
    #     return dataframe.set_index('idx')