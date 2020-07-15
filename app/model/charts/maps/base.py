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

    def add_au_marker(self, map, dataframe, au, options, chart_options):
        # Adding marker to current analysis unit
        if np.issubdtype(dataframe.index.dtype, np.number):
            au = int(au)

        au_row = dataframe.loc[au].reset_index().iloc[0]
        
        au_title = 'Analysis Unit'
        if len(options.get('headers', [])) > 0:
            au_title = au_row[options.get('headers', [])[0]['value']]

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