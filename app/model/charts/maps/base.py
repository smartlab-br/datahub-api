''' Base class for maps '''
import folium
import numpy as np
from service.viewconf_reader import ViewConfReader

class BaseMap():
    ''' Base class for maps '''
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

    @staticmethod
    def add_au_marker(folium_map, dataframe, analysis_unit, options, chart_options):
        ''' Adds a marker for current analysis unit in the map '''
        # Adding marker to current analysis unit
        if np.issubdtype(dataframe.index.dtype, np.number):
            analysis_unit = int(analysis_unit)

        au_row = dataframe.loc[analysis_unit].reset_index().iloc[0]

        centroide = None
        if chart_options.get('lat', 'latitude') in list(dataframe.columns):
            centroide = [
                au_row[chart_options.get('lat', 'latitude')].item(),
                au_row[chart_options.get('long', 'longitude')].item()
            ]

        if centroide:
            marker_layer = folium.map.FeatureGroup(
                name=self.get_au_title(au_row, options.get('headers'))
            )
            folium.map.Marker(
                centroide,
                tooltip=au_row.get('tooltip', "Tooltip!"),
                icon=folium.Icon(color=ViewConfReader.get_marker_color(options))
            ).add_to(marker_layer)
            marker_layer.add_to(folium_map)
        return folium_map

    def post_adjustments(self, folium_map, dataframe, chart_options):
        ''' Adds final configurations to map, such as bounds and layer control '''
        folium.LayerControl().add_to(folium_map)
        folium_map.get_root().header.add_child(folium.Element(self.STYLE_STATEMENT))

        # Getting bounds from dataframe
        folium_map.fit_bounds([
            [
                dataframe[chart_options.get('lat', 'latitude')].min(),
                dataframe[chart_options.get('long', 'longitude')].min()
            ],
            [
                dataframe[chart_options.get('lat', 'latitude')].max(),
                dataframe[chart_options.get('long', 'longitude')].max()
            ]
        ])
        return folium_map

    @staticmethod
    def get_headers(chart_options, options):
        ''' Chooses whether to use given headers config or infer from options '''
        if 'headers' in options:
            return options.get('headers')
        if chart_options is None:
            return [{'text': 'Analysis Unit', 'value': 'nm_municipio'}]
        return ViewConfReader.get_headers_from_options_descriptor(
            options.get('description'),
            [{
                'text': 'Analysis Unit',
                'value': chart_options.get('name_field', 'nm_municipio')
            }]
        )

    def get_tooltip_data(self, dataframe, chart_options, options):
        ''' Creates tooltip content series from given options and dataframe '''
        # Get pivoted dataframe for tooltip list creation
        df_tooltip = dataframe.copy().pivot_table(
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
        if options is not None:
            headers = options.get("headers")

        df_tooltip['tooltip'] = df_tooltip.apply(
            self.tooltip_gen,
            headers=headers,
            axis=1
        )
        return df_tooltip[[chart_options.get('id_field', 'cd_mun_ibge'), 'tooltip']]

    @staticmethod
    def get_location_columns(chart_options):
        ''' Get the column names to use as reference to location and value in the dataframe '''
        if chart_options is None:
            return ['lat', 'long']
        cols = [chart_options.get('lat', 'lat'), chart_options.get('long', 'long')]
        if 'value_field' in chart_options:
            cols.append(chart_options.get('value_field'))
        return cols

    @staticmethod
    def prepare_dataframe(dataframe, chart_options, tooltip_data=None):
        ''' Creates a standard index for the dataframes '''
        if chart_options is None:
            return dataframe

        # Adding tooltips to detailed dataframe
        if tooltip_data is not None:
            dataframe = pd.merge(
                dataframe,
                tooltip_data,
                left_on=chart_options.get('id_field', 'cd_mun_ibge'),
                right_on=chart_options.get('id_field', 'cd_mun_ibge'),
                how="left"
            )

        dataframe['str_id'] = dataframe[chart_options.get('id_field', 'cd_mun_ibge')].astype(str)
        dataframe['idx'] = dataframe[chart_options.get('id_field', 'cd_mun_ibge')]
        return dataframe.set_index('idx')

    @staticmethod
    def tooltip_gen(row, **kwargs):
        ''' Generates marker tooltip based on the location and collection of fields
            sent on "headers" option '''
        headers = kwargs.get('headers')
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
        ''' Gets the analysis unit title from headers definition '''
        if headers is None or len(headers) <= 0 or row is None:
            return 'Analysis Unit'
        return row[headers[0].get('value')]
