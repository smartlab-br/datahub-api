""" Base class for maps """
import folium
import numpy as np
import pandas as pd
from service.viewconf_reader import ViewConfReader


class BaseMap():
    """ Base class for maps """
    TILES_URL = 'https://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}'
    TILES_ATTRIBUTION = 'Esri, USGS | Esri, HERE | Esri, Garmin, FAO, NOAA'

    STYLE_STATEMENT = "\
        <link href='https://fonts.googleapis.com/css2?family=Pathway+Gothic+One&display=swap' \
            rel='stylesheet'>\
        <style>\
            .legend.leaflet-control{display:none}\
            .leaflet-tooltip table tbody tr:first-child th, \
            .leaflet-popup table tbody tr:first-child th{display:none;}\
            .leaflet-tooltip table tbody tr:first-child td, \
            .leaflet-popup table tbody tr:first-child td{\
                font-family: 'Pathway Gothic One', Calibri, sans-serif;\
                font-size: 2.5em;\
                font-weight: 700;\
            }\
            .leaflet-popup table tbody tr:nth-child(2), \
            .leaflet-tooltip table tbody tr:nth-child(2){\
                border-top: 1px solid black;\
            }\
            path.leaflet-interactive:hover {\
                fill-opacity: 1;\
            }\
        </style>"

    def add_au_marker(self, folium_map, analysis_unit):
        """ Adds a marker for current analysis unit in the map """
        # Adding marker to current analysis unit
        if np.issubdtype(self.dataframe.index.dtype, np.number):
            analysis_unit = int(analysis_unit)

        au_row = self.dataframe.loc[analysis_unit].reset_index().iloc[0]

        centroide = None
        if self.options.get('chart_options', {}).get('lat', 'latitude') in list(self.dataframe.columns):
            centroide = [
                au_row[self.options.get('chart_options', {}).get('lat', 'latitude')].item(),
                au_row[self.options.get('chart_options', {}).get('long', 'longitude')].item()
            ]

        if centroide:
            marker_layer = folium.map.FeatureGroup(
                name=self.get_au_title(au_row, self.options.get('headers'))
            )
            folium.map.Marker(
                centroide,
                tooltip=au_row.get('tooltip', "Tooltip!"),
                icon=folium.Icon(color=ViewConfReader.get_marker_color(self.options))
            ).add_to(marker_layer)
            marker_layer.add_to(folium_map)
        return folium_map

    def post_adjustments(self, folium_map):
        """ Adds final configurations to map, such as bounds and layer control """
        folium.LayerControl().add_to(folium_map)
        folium_map.get_root().header.add_child(folium.Element(self.STYLE_STATEMENT))

        # Getting bounds from dataframe
        chart_options = self.options.get('chart_options', {})
        folium_map.fit_bounds([
            [
                self.dataframe[chart_options.get('lat', 'latitude')].min(),
                self.dataframe[chart_options.get('long', 'longitude')].min()
            ],
            [
                self.dataframe[chart_options.get('lat', 'latitude')].max(),
                self.dataframe[chart_options.get('long', 'longitude')].max()
            ]
        ])
        return folium_map

    def get_headers(self):
        """ Chooses whether to use given headers config or infer from options """
        if 'headers' in self.options:
            return self.options.get('headers')
        if 'chart_options' in self.options:
            return [{'text': '', 'value': 'nm_municipio'}]
        return ViewConfReader.get_headers_from_options_descriptor(
            self.options.get('description'),
            [{
                'text': '',
                'value': self.options.get('chart_options', {}).get('name_field', 'nm_municipio')
            }]
        )

    def get_tooltip_data(self):
        """ Creates tooltip content series from given options and dataframe """
        # Get pivoted dataframe for tooltip list creation
        chart_options = self.options.get('chart_options', {})
        df_tooltip = self.dataframe.copy().pivot_table(
            index=[
                chart_options.get('id_field', 'cd_mun_ibge'),
                chart_options.get('name_field', 'nm_municipio'),
                chart_options.get('lat', 'latitude'),
                chart_options.get('long', 'longitude')
            ],
            columns='cd_indicador',
            fill_value=0
        )
        df_tooltip.columns = ['_'.join(reversed(col)).strip() for col in df_tooltip.columns.values]
        df_tooltip = df_tooltip.reset_index()

        # Merge dataframe and pivoted dataframe
        headers = None
        if self.options is not None:
            headers = self.options.get("headers")

        df_tooltip['tooltip'] = df_tooltip.apply(
            self.tooltip_gen,
            headers=headers,
            axis=1
        )
        return df_tooltip[[chart_options.get('id_field', 'cd_mun_ibge'), 'tooltip']]

    def get_location_columns(self):
        """ Get the column names to use as reference to location and value in the dataframe """
        chart_options = self.options.get('chart_options')
        if chart_options is None:
            return ['lat', 'long']
        cols = [chart_options.get('lat', 'lat'), chart_options.get('long', 'long')]
        if 'value_field' in chart_options:
            cols.append(chart_options.get('value_field'))
        return cols

    def prepare_dataframe(self, tooltip_data=None):
        """ Creates a standard index for the dataframes """
        chart_options = self.options.get('chart_options')
        if chart_options is None:
            return self.dataframe

        # Adding tooltips to detailed dataframe
        if tooltip_data is not None:
            self.dataframe = pd.merge(
                self.dataframe,
                tooltip_data,
                left_on=chart_options.get('id_field', 'cd_mun_ibge'),
                right_on=chart_options.get('id_field', 'cd_mun_ibge'),
                how="left"
            )

        self.dataframe['str_id'] = self.dataframe[chart_options.get('id_field', 'cd_mun_ibge')].astype(str)
        self.dataframe['idx'] = self.dataframe[chart_options.get('id_field', 'cd_mun_ibge')]
        self.dataframe.set_index('idx')

    @staticmethod
    def tooltip_gen(row, headers):
        """ Generates marker tooltip based on the location and collection of fields
            sent on "headers" option """
        if headers is None or row is None:
            return "Tooltip!"
        tooltip = "".join([
            f"<tr style='text-align: left;'><th style='padding: 4px; padding-right: 10px;'>{hdr.get('text').encode('ascii', 'xmlcharrefreplace').decode()}</th><td style='padding: 4px;'>{str(row[hdr.get('value')]).encode('ascii', 'xmlcharrefreplace').decode()}</td></tr>"
            for
            hdr
            in
            headers
        ])
        return f"<table>{tooltip}</table>"

    @staticmethod
    def get_au_title(row, headers):
        """ Gets the analysis unit title from headers definition """
        if headers is None or len(headers) <= 0 or row is None:
            return 'Analysis Unit'
        return row[headers[0].get('value')]

    def pre_draw(self, tooltip_data):
        """ Common setup for dataframe and map """
        self.options['headers'] = self.get_headers()
        self.prepare_dataframe(tooltip_data),
        return folium.Map(
            tiles=self.TILES_URL,
            attr=self.TILES_ATTRIBUTION,
            control_scale=True
        )
