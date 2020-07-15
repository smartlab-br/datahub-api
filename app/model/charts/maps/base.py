''' Base class for maps '''
import folium
import numpy as np
import pandas as pd
from service.viewconf_reader import ViewConfReader

class BaseMap():
    ''' Base class for maps '''
    TILES_URL = 'https://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}'
    TILES_ATTRIBUTION = 'Esri, USGS | Esri, HERE | Esri, Garmin, FAO, NOAA'

    STYLE_STATEMENT = "<link href='https://fonts.googleapis.com/css2?family=Pathway+Gothic+One&display=swap' rel='stylesheet'>\
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

    @staticmethod
    def add_au_marker(map, dataframe, au, options, chart_options):
        # Adding marker to current analysis unit
        if np.issubdtype(dataframe.index.dtype, np.number):
            au = int(au)

        au_row = dataframe.loc[au].reset_index().iloc[0]
        
        au_title = 'Analysis Unit'
        if len(options.get('headers', [])) > 0:
            au_title = au_row[options.get('headers', [])[0]['value']]

        centroide = None
        if chart_options.get('lat','latitude') in list(dataframe.columns):
            centroide = [au_row[chart_options.get('lat','latitude')].item(), au_row[chart_options.get('long','longitude')].item()]
            
        if centroide:
            marker_layer = folium.map.FeatureGroup(name = au_title)
            folium.map.Marker(
                centroide,
                tooltip=au_row.get('tooltip', "Tooltip!"),
                icon=folium.Icon(color=ViewConfReader.get_marker_color(options))
            ).add_to(marker_layer)
            marker_layer.add_to(map)
        return map

    @staticmethod
    def post_adjustments(map, dataframe, chart_options):
        folium.LayerControl().add_to(map)
        map.get_root().header.add_child(folium.Element(self.STYLE_STATEMENT))

        # Getting bounds from dataframe
        map.fit_bounds([
            [
                dataframe[chart_options.get('lat','latitude')].min(),
                dataframe[chart_options.get('long','longitude')].min()
            ],
            [
                dataframe[chart_options.get('lat','latitude')].max(),
                dataframe[chart_options.get('long','longitude')].max()
            ]
        ])
        return map

    @staticmethod
    def get_headers(chart_options, options):
        if 'headers' in options:
            return options.get('headers')
        return ViewConfReader.get_headers_from_options_descriptor(
            options.get('description'),
            [{
                'text': 'Analysis Unit',
                'value': chart_options.get('name_field', 'nm_municipio')
            }]
        )

    @staticmethod
    def get_tooltip_data(dataframe, chart_options, options):
        # Get pivoted dataframe for tooltip list creation
        df_tooltip = dataframe.copy().pivot_table(
            index=[chart_options.get('id_field','cd_mun_ibge'), chart_options.get('name_field', 'nm_municipio'), chart_options.get('lat','latitude'), chart_options.get('long','longitude')],
            columns='cd_indicador',
            fill_value=0
        )
        df_tooltip.columns = ['_'.join(reversed(col)).strip() for col in df_tooltip.columns.values]
        df_tooltip = df_tooltip.reset_index()
        
        # Tooltip gen function
        def tooltip_gen(au_row, **kwargs):
            if 'headers' in options:
                marker_tooltip = "".join([f"<tr style='text-align: left;'><th style='padding: 4px; padding-right: 10px;'>{hdr.get('text').encode('ascii', 'xmlcharrefreplace').decode()}</th><td style='padding: 4px;'>{str(au_row[hdr.get('value')]).encode('ascii', 'xmlcharrefreplace').decode()}</td></tr>" for hdr in kwargs.get('headers')])
                return f"<table>{marker_tooltip}</table>"
            return "Tooltip!"
        
        # Merge dataframe and pivoted dataframe
        df_tooltip['tooltip'] = df_tooltip.apply(
            tooltip_gen,
            headers= options.get("headers"),
            axis=1
        )
        return df_tooltip[[chart_options.get('id_field', 'cd_mun_ibge'), 'tooltip']]

    @staticmethod
    def get_location_columns(chart_options):
        cols = [chart_options.get('lat','lat'), chart_options.get('long','long')]
        if 'value_field' in chart_options:
            cols.append(chart_options.get('value_field'))
        return cols

    @staticmethod
    def prepare_dataframe(dataframe, chart_options):
        dataframe['str_id'] = dataframe[chart_options.get('id_field', 'cd_mun_ibge')].astype(str)
        dataframe['idx'] = dataframe[chart_options.get('id_field', 'cd_mun_ibge')]
        return dataframe.set_index('idx')
        