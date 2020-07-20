'''Main tests in API'''
import unittest
import pandas as pd
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
            options.get('headers')
        )

    def test_existing_headers(self):
        ''' Tests if returns the existing headers AS-IS '''
        options = {'headers': {'name': 'test'}}
        self.assertEqual(
            BaseMap.get_headers({'name_field': 'au_field'}, options),
            options.get('headers')
        )

    def test_existing_headers_over_description(self):
        ''' Tests if headers prevails when there's also description option '''
        options = {'headers': {'name': 'test'}, 'description': self.BASE_DESCRIPTION}
        self.assertEqual(
            BaseMap.get_headers({'name_field': 'au_field'}, options),
            options.get('headers')
        )
    
    def test_existing_description_no_chart_options(self):
        ''' Tests if returns the expected result, with default 'nm_municipio' header
            when no chart_option is sent '''
        options = {'description': self.BASE_DESCRIPTION}
        self.assertEqual(
            BaseMap.get_headers(None, options),
            [{'text': 'Analysis Unit', 'value': 'nm_municipio'}]
        )

    def test_existing_description(self):
        ''' Tests if returns the expected header build using card description options '''
        options = {'description': self.BASE_DESCRIPTION}
        expect = [{'text': 'Analysis Unit', 'value': 'au_field'}]
        expect.extend(self.BASE_EXPECT)
        self.assertEqual(
            BaseMap.get_headers({'name_field': 'au_field'}, options),
            expect
        )

    def test_existing_description_default_au_field(self):
        ''' Tests if returns the expected result, with default 'nm_municipio' header
            when there's no name_field attribute in chart_options '''
        options = {'description': self.BASE_DESCRIPTION}
        expect = [{'text': 'Analysis Unit', 'value': 'nm_municipio'}]
        expect.extend(self.BASE_EXPECT)
        self.assertEqual(BaseMap.get_headers({}, options), expect)

class BaseMapGetLocationColumnsTest(unittest.TestCase):
    ''' Test behaviours linked to fetching locations and value columns '''
    def test_default_lat_long_no_options(self):
        ''' Tests for default lat and long fields, with no value column definition,
            when no chart_options is given '''
        self.assertEqual(BaseMap.get_location_columns(None), ['lat','long'])

    def test_default_lat_long(self):
        ''' Tests for default lat and long fields, with no value column definition '''
        self.assertEqual(BaseMap.get_location_columns({}), ['lat','long'])

    def test_default_lat_long_value(self):
        ''' Tests for default lat and long fields, with given value column definition '''
        self.assertEqual(
            BaseMap.get_location_columns({'value_field': 'val'}),
            ['lat','long', 'val']
        )

    def test_given_lat_long(self):
        ''' Tests lat and long columns retrieval, with no given value column definition '''
        self.assertEqual(
            BaseMap.get_location_columns({'lat': 'latitude', 'long': 'longitude'}),
            ['latitude','longitude']
        )

    def test_given_lat_long_val(self):
        ''' Tests lat, long and value columns retrieval '''
        self.assertEqual(
            BaseMap.get_location_columns({
                'lat': 'latitude', 'long': 'longitude', 'value_field': 'val'
            }),
            ['latitude','longitude', 'val']
        )

class BaseMapPrepareDataframeTest(unittest.TestCase):
    ''' Test behaviours linked to adding index and stringified index to a dataframe '''
    DATAFRAME = pd.DataFrame([
        {"cd_mun_ibge": 123456, 'cd_indicador': 1},
        {"cd_mun_ibge": 234567, 'cd_indicador': 2},
        {"cd_mun_ibge": 345678, 'cd_indicador': 3}
    ])
    def test_prepare_no_options(self):
        ''' Tests if dataframe returns AS-IS if no options are given '''
        self.assertEqual(
            BaseMap.prepare_dataframe(self.DATAFRAME.copy(), None).to_dict(orient="records"),
            self.DATAFRAME.copy().to_dict(orient="records")       
        )
 
    def test_prepare_no_id_field(self):
        ''' Tests if dataframe returns default options if no identifier is given '''
        result = BaseMap.prepare_dataframe(self.DATAFRAME.copy(), {})
        self.assertEqual(
            result.copy().to_dict(orient="records"),
            [
                {"cd_mun_ibge": 123456, 'cd_indicador': 1, 'str_id': '123456'},
                {"cd_mun_ibge": 234567, 'cd_indicador': 2, 'str_id': '234567'},
                {"cd_mun_ibge": 345678, 'cd_indicador': 3, 'str_id': '345678'}
            ]       
        )
        result = result.reset_index()
        self.assertEqual(
            result.to_dict(orient="records"),
            [
                {"cd_mun_ibge": 123456, 'cd_indicador': 1, 'idx': 123456, 'str_id': '123456'},
                {"cd_mun_ibge": 234567, 'cd_indicador': 2, 'idx': 234567, 'str_id': '234567'},
                {"cd_mun_ibge": 345678, 'cd_indicador': 3, 'idx': 345678, 'str_id': '345678'}
            ]       
        )

    def test_prepare_id_field(self):
        ''' Tests if dataframe returns dataframe with index and stringified index
            accrding to given id field '''
        result = BaseMap.prepare_dataframe(self.DATAFRAME.copy(), {"id_field": "cd_indicador"})
        self.assertEqual(
            result.copy().to_dict(orient="records"),
            [
                {"cd_mun_ibge": 123456, 'cd_indicador': 1, 'str_id': '1'},
                {"cd_mun_ibge": 234567, 'cd_indicador': 2, 'str_id': '2'},
                {"cd_mun_ibge": 345678, 'cd_indicador': 3, 'str_id': '3'}
            ]       
        )
        result = result.reset_index()
        self.assertEqual(
            result.to_dict(orient="records"),
            [
                {"cd_mun_ibge": 123456, 'cd_indicador': 1, 'idx': 1, 'str_id': '1'},
                {"cd_mun_ibge": 234567, 'cd_indicador': 2, 'idx': 2, 'str_id': '2'},
                {"cd_mun_ibge": 345678, 'cd_indicador': 3, 'idx': 3, 'str_id': '3'}
            ]       
        )

class BaseMapGetTooltipDataTest(unittest.TestCase):
    ''' Test behaviours linked to fetching tooltip series based on given configuration '''
    DATAFRAME = pd.DataFrame([
        {
            'cd_indicador': 'A',
            'cd_mun_ibge': 123456,
            'nm_municipio': 'Emerald City',
            'latitude': 180,
            'longitude': 720,
            'vl_indicador': 1
        },
        {
            'cd_indicador': 'A',
            'cd_mun_ibge': 234567,
            'nm_municipio': 'Badlands',
            'latitude': -180,
            'longitude': -720,
            'vl_indicador': -1
        },
        {
            'cd_indicador': 'B',
            'cd_mun_ibge': 123456,
            'nm_municipio': 'Emerald City',
            'latitude': 180,
            'longitude': 720,
            'vl_indicador': 2
        },
        {
            'cd_indicador': 'B',
            'cd_mun_ibge': 234567,
            'nm_municipio': 'Badlands',
            'latitude': -180,
            'longitude': -720,
            'vl_indicador': -2
        },
    ])
    EXPECT = [
        {
            'cd_mun_ibge': 123456,
            'tooltip': "<table>"
                        "<tr style='text-align: left;'>"
                        "<th style='padding: 4px; padding-right: 10px;'>Municipio:</th>"
                        "<td style='padding: 4px;'>Emerald City</td>"
                        "</tr>"
                        "<tr style='text-align: left;'>"
                        "<th style='padding: 4px; padding-right: 10px;'>Valor A:</th>"
                        "<td style='padding: 4px;'>1</td>"
                        "</tr>"
                        "<tr style='text-align: left;'>"
                        "<th style='padding: 4px; padding-right: 10px;'>Valor B:</th>"
                        "<td style='padding: 4px;'>2</td>"
                        "</tr>"
                        "</table>"
        },
        {
            'cd_mun_ibge': 234567,
            'tooltip': "<table>"
                        "<tr style='text-align: left;'>"
                        "<th style='padding: 4px; padding-right: 10px;'>Municipio:</th>"
                        "<td style='padding: 4px;'>Badlands</td>"
                        "</tr>"
                        "<tr style='text-align: left;'>"
                        "<th style='padding: 4px; padding-right: 10px;'>Valor A:</th>"
                        "<td style='padding: 4px;'>-1</td>"
                        "</tr>"
                        "<tr style='text-align: left;'>"
                        "<th style='padding: 4px; padding-right: 10px;'>Valor B:</th>"
                        "<td style='padding: 4px;'>-2</td>"
                        "</tr>"
                        "</table>"
        }
    ]
    def test_no_options(self):
        ''' Tests if a default tooltip text is set for all items if no options are given '''
        BaseMap.get_tooltip_data(self.DATAFRAME.copy(), {}, None)
        self.assertEqual(
            BaseMap.get_tooltip_data(self.DATAFRAME.copy(), {}, None).to_dict(orient="records"),
            [
                {'cd_mun_ibge': 123456, 'tooltip': "Tooltip!"},
                {'cd_mun_ibge': 234567, 'tooltip': "Tooltip!"}
            ]
        )
    
    def test_no_headers(self):
        ''' Tests if a default tooltip text is set for all items if no headers are given '''
        self.assertEqual(
            BaseMap.get_tooltip_data(self.DATAFRAME.copy(), {}, {}).to_dict(orient="records"),
            [
                {'cd_mun_ibge': 123456, 'tooltip': "Tooltip!"},
                {'cd_mun_ibge': 234567, 'tooltip': "Tooltip!"}
            ]
        )

    def test_headers(self):
        ''' Tests if a default tooltip text is set for all items if no headers are given '''
        self.assertEqual(
            BaseMap.get_tooltip_data(
                self.DATAFRAME.copy(),
                {},
                {"headers": [
                    {'text': 'Municipio:', 'value': 'nm_municipio'},
                    {'text': 'Valor A:', 'value': 'A_vl_indicador'},
                    {'text': 'Valor B:', 'value': 'B_vl_indicador'}
                ]}
            ).to_dict(orient="records"),
            self.EXPECT
        )

    def test_headers_custom_fields(self):
        ''' Tests if a default tooltip text is set for all items if no headers are given '''
        dataframe = self.DATAFRAME.rename(columns={
            'cd_mun_ibge': 'cd_m',
            'nm_municipio': 'nm_m',
            'latitude': 'lat',
            'longitude': 'long'
        })
        
        expect = self.EXPECT.copy()
        for item in expect:
            item['cd_m'] = item['cd_mun_ibge']
            del item['cd_mun_ibge']

        self.maxDiff = None
        self.assertEqual(
            BaseMap.get_tooltip_data(
                dataframe,
                {'id_field': 'cd_m', 'name_field': 'nm_m', 'lat': 'lat', 'long': 'long'},
                {"headers": [
                    {'text': 'Municipio:', 'value': 'nm_m'},
                    {'text': 'Valor A:', 'value': 'A_vl_indicador'},
                    {'text': 'Valor B:', 'value': 'B_vl_indicador'}
                ]}
            ).to_dict(orient="records"),
            expect
        )
    # @staticmethod
    # def get_tooltip_data(dataframe, chart_options, options):
    #     ''' Creates tooltip content series from given options and dataframe '''
    #     # Get pivoted dataframe for tooltip list creation
    #     df_tooltip = dataframe.copy().pivot_table(
    #         index=[
    #             chart_options.get('id_field', 'cd_mun_ibge'),
    #             chart_options.get('name_field', 'nm_municipio'),
    #             chart_options.get('lat', 'latitude'),
    #             chart_options.get('long', 'longitude')
    #         ],
    #         columns='cd_indicador',
    #         fill_value=0
    #     )
    #     df_tooltip.columns = ['_'.join(reversed(col)).strip() for col in df_tooltip.columns.values]
    #     df_tooltip = df_tooltip.reset_index()
    #     # Tooltip gen function
    #     def tooltip_gen(au_row, **kwargs):
    #         if 'headers' in options:
    #             marker_tooltip = "".join([
    #                 f"<tr style='text-align: left;'><th style='padding: 4px; padding-right: 10px;'>{hdr.get('text').encode('ascii', 'xmlcharrefreplace').decode()}</th><td style='padding: 4px;'>{str(au_row[hdr.get('value')]).encode('ascii', 'xmlcharrefreplace').decode()}</td></tr>"
    #                 for
    #                 hdr
    #                 in
    #                 kwargs.get('headers')
    #             ])
    #             return f"<table>{marker_tooltip}</table>"
    #         return "Tooltip!"
    #     # Merge dataframe and pivoted dataframe
    #     df_tooltip['tooltip'] = df_tooltip.apply(
    #         tooltip_gen,
    #         headers=options.get("headers"),
    #         axis=1
    #     )
    #     return df_tooltip[[chart_options.get('id_field', 'cd_mun_ibge'), 'tooltip']]
