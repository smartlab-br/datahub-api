''' Model for fetching chart '''
import matplotlib.pyplot as plt
import numpy as np
import io
import folium
import json
import requests
from service.viewconf_reader import ViewConfReader
import os
import time
from service.charts.maps.base import BaseMap
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import html

class Choropleth(BaseMap):
    ''' Choropleth building class '''
    def draw(self, dataframe, options):
        ''' Gera um mapa topojson a partir das opções enviadas '''
        # http://localhost:5000/charts/choropleth?from_viewconf=S&au=2927408&card_id=mapa_pib_brasil&dimension=socialeconomico&as_image=S
        visao = options.get('visao', 'uf')

        style_statement = "<link href='https://fonts.googleapis.com/css2?family=Pathway+Gothic+One&display=swap' rel='stylesheet'>\
            <style>\
                .legend.leaflet-control{display:none}\
                .leaflet-tooltip table tbody tr:first-child th{display:none;}\
                .leaflet-tooltip table tbody tr:first-child td{\
                    font-family: 'Pathway Gothic One', Calibri, sans-serif;\
                    font-size: 2.5em;\
                    font-weight: 700;\
                }\
                .leaflet-tooltip table tbody tr:nth-child(2){\
                    border-top: 1px solid black;\
                }\
                path.leaflet-interactive:hover {\
                    fill-opacity: 1;\
                }\
            </style>"

        au = options.get('au')
        chart_options = options.get('chart_options')

        # Gets the geojson
        quality = options.get('chart_options', {}).get('quality','1')
        if len(str(au)) > 2:
            cd_uf=str(au)[:2]
            res = 'municipio'
            state_geo = f'https://raw.githubusercontent.com/smartlab-br/geodata/master/topojson/br/{visao}/{res}/{cd_uf}_q{quality}.json'
        elif len(str(au)) == 2 and options.get('chart_options', {}).get('topology') == 'uf':
            state_geo = f'https://raw.githubusercontent.com/smartlab-br/geodata/master/topojson/br/uf_q{quality}.json'
        # Trocar por topojson dos estados no Brasil
        elif (res == visao):
            state_geo = f'https://raw.githubusercontent.com/smartlab-br/geodata/master/topojson/br/{visao}/{au}_q{quality}.json'
        else:
            state_geo = f'https://raw.githubusercontent.com/smartlab-br/geodata/master/topojson/br/{visao}/{res}/{au}_q{quality}.json' 
        state_geo = requests.get(state_geo).json()
        
        dataframe['str_id'] = dataframe[chart_options.get('id_field')].astype(str)
        dataframe['idx'] = dataframe[chart_options.get('id_field')]
        
        # Runs dataframe modifiers from viewconf
        dataframe = ViewConfReader().generate_columns(dataframe, options)

        dataframe = dataframe.set_index('idx')
        centroide = None  
        marker_tooltip = ''
        # for each_au in state_geo.get('features'):
        for each_au in state_geo.get('objects',{}).get('data',{}).get('geometries',[]):
            # During topo conversion, all ID will be named smartlab_geo_id and
            # all NAME will be in an attribute called smartlab_geo_name.
            try:
                df_row = dataframe.loc[int(each_au.get('properties').get("smartlab_geo_id"))]
                each_au.get('properties').update(json.loads(df_row.to_json()), headers=options.get('headers'))
            except KeyError:
                df_row = {hdr.get('value'): 'N/A' for hdr in options.get('headers')}
                df_row[options.get('headers')[0].get('value')] = each_au.get('properties').get('smartlab_geo_name')
                each_au.get('properties').update(json.loads(json.dumps(df_row)), headers=options.get('headers'))
            if str(each_au.get('properties', {}).get(chart_options.get('id_field'))) == str(au):
                centroide = each_au.get('properties', {}).get('centroide')
                if centroide:
                    centroide.reverse()
                
                marker_tooltip = "".join([f"<tr style='text-align: left;'><th style='padding: 4px; padding-right: 10px;'>{hdr.get('text').encode('ascii', 'xmlcharrefreplace').decode()}</th><td style='padding: 4px;'>{str(df_row[hdr.get('value')]).encode('ascii', 'xmlcharrefreplace').decode()}</td></tr>" for hdr in options.get('headers')])
                marker_tooltip = f"<table>{marker_tooltip}</table>"
        
        # Creating map instance
        n = folium.Map(tiles=self.TILES_URL, attr = self.TILES_ATTRIBUTION, control_scale = True)

        # Creating the choropleth layer
        color_scale = ViewConfReader.get_color_scale(
            options,
            dataframe[chart_options['value_field']].min(), 
            dataframe[chart_options['value_field']].max()
        )
        def get_color(feature):
            if feature is None:
                return '#8c8c8c' # MISSING -> gray
            value = None
            if chart_options['value_field'] in feature.get('properties',{}):
                value = feature.get('properties',{}).get(chart_options['value_field'])
            if value is None:
                return '#8c8c8c' # MISSING -> gray
            else:
                return color_scale(value)

        chart = folium.TopoJson(
            state_geo,
            'objects.data',
            name=ViewConfReader.get_chart_title(options),
            style_function = lambda feature: {
                'fillColor': get_color(feature),
                'fillOpacity': 0.8,
                'color' : 'black',
                'stroke' : 'black',
                'lineOpacity': 0.2,
                'weight' : 0.2,
            }
        )

        # Adding tooltip to choropleth
        folium.features.GeoJsonTooltip(
            fields = [hdr.get('value') for hdr in options.get('headers')],
            aliases = [hdr.get('text') for hdr in options.get('headers')],
            localize=True,
            sticky=False,
            labels=True
        ).add_to(chart)

        # Adding marker to current analysis unit
        if np.issubdtype(dataframe.index.dtype, np.number):
            au = int(au)
        au_row = dataframe.loc[au]
        au_title = 'Analysis Unit'
        if len(options.get('headers', [])) > 0:
            au_title = au_row[options.get('headers', [])[0]['value']]

        if 'latitude' in list(dataframe.columns):
            centroide = [au_row['latitude'], au_row['longitude']]
        
        if centroide:
            marker_layer = folium.map.FeatureGroup(name = au_title)
            folium.map.Marker(
                centroide,
                tooltip=marker_tooltip,
                icon=folium.Icon(color=ViewConfReader.get_marker_color(options))
            ).add_to(marker_layer)
            marker_layer.add_to(n)
        
        chart.add_to(n)
        folium.LayerControl().add_to(n)

        n.get_root().header.add_child(folium.Element(self.STYLE_STATEMENT))

        # Getting bounds from topojson
        lower_left = state_geo.get('bbox')[:2]
        lower_left.reverse()
        upper_right = state_geo.get('bbox')[2:]
        upper_right.reverse()
        # Zooming to bounds
        n.fit_bounds([lower_left, upper_right])

        return n
