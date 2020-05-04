''' Model for fetching chart '''
from model.base import BaseModel
from model.thematic import Thematic
import matplotlib.pyplot as plt
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.io import export_png
from bokeh.io.export import get_screenshot_as_png
import io
import folium
import json
import requests
from service.viewconf_reader import ViewConfReader
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import html

class Chart(BaseModel):
    ''' Model for fetching dinamic and static charts '''
    CHART_LIB_DEF = {
        'FOLIUM': ['MAP_TOPOJSON']
    } # Defaults to BOKEH
    def get_chart(self, options):
        ''' Selects if the chart should be static or dynamic '''
        options['as_pandas'] = True
        options['no_wrap'] = True

        if options.get('from_viewconf'):
            added_options = ViewConfReader.set_custom_options(options)
            struct = ViewConfReader().get_card_descriptor(
                options.get('language', 'br'),
                options.get('observatory', 'td'),
                options.get('scope', 'municipio'),
                options.get('dimension'),
                options.get('card_id')
            )

            options = {**options, **ViewConfReader.api_to_options(struct.get('api'), {**options, **added_options}), **struct}
            dataframe = Thematic().find_dataset({**{'as_pandas': True, 'no_wrap': True}, **ViewConfReader.api_to_options(struct.get('api'), {**options, **added_options})})
        else:
            dataframe = Thematic().find_dataset(options)
        
        chart = self.get_raw_chart(dataframe, options)
        
        chart_lib = 'BOKEH'
        for chart_key, chart_types in self.CHART_LIB_DEF.items():
            if options.get('chart_type') in chart_types:
                chart_lib = chart_key

        if options.get('as_image'):
            return self.get_image(chart, chart_lib)
        return self.get_dynamic_chart(chart, chart_lib)

    def get_raw_chart(self, dataframe, options):
        ''' Selects and loads the chart '''
        if options.get('chart_type') == 'scatter':
            return self.draw_scatter(dataframe, options)
        if options.get('chart_type') == 'MAP_TOPOJSON':
            return self.draw_choropleth(dataframe, options)
        pass
        
    @staticmethod
    def get_image(chart, lib):
        ''' Gets chart as image '''
        if lib == 'BOKEH':
            img = get_screenshot_as_png(chart)
            roiImg = img.crop()
            imgByteArr = io.BytesIO()
            
            roiImg.save(imgByteArr, format='PNG')
            return imgByteArr.getvalue()
        elif lib == 'FOLIUM':
            ff_options = Options()
            ff_options.set_headless(headless=True)
            
            cap = DesiredCapabilities().FIREFOX
            cap["marionette"] = True
            driver = webdriver.Firefox(firefox_options=ff_options, capabilities=cap)
            
            driver.get("data:text/html;charset=utf-8,{html_content}".format(html_content=chart._repr_html_()))
            
            return driver.get_screenshot_as_png()
        pass

    @staticmethod
    def get_dynamic_chart(chart, lib):
        ''' Gets dynamic chart '''
        # /charts?theme=teindicadoresmunicipais&categorias=ds_agreg_primaria&valor=vl_indicador&agregacao=SUM&filtros=eq-cd_mun_ibge-2927408,and,eq-cd_indicador-%27te_nat_ocup_atual%27
        if lib == 'BOKEH':
            (script, div) = components(chart)
            return {'script': script, 'div': div}
        elif lib == 'FOLIUM':
            return {'div': chart._repr_html_(), 'mime': 'text/html'}
        pass

    @staticmethod
    def draw_scatter(dataframe, options):
        ''' Draws the scatterplot '''
        # http://localhost:5000/charts/scatter?theme=sstindicadoresestaduais&categorias=ds_agreg_primaria-v,ds_agreg_secundaria-x,vl_indicador-y&filtros=eq-nu_competencia-2017,and,eq-cd_indicador-%27sst_bene_sexo_idade_dias_perdidos%27&as_image=S
        colormap = {'Feminino': 'red', 'Masculino': 'blue', 'Indefinido': 'pink'}
        chart = figure()
        chart.circle(
            dataframe["x"], dataframe["y"],
            color=[colormap[x] for x in dataframe['v']],
            fill_alpha=0.2, size=10)

        # output_file("iris.html", title="iris.py example")
        return chart

    @staticmethod
    def draw_choropleth(dataframe, options):
        ''' Gera um mapa topojson a partir das opções enviadas '''
        # http://localhost:5000/charts/choropleth?from_viewconf=S&au=2927408&card_id=mapa_pib_brasil&dimension=socialeconomico&as_image=S
        # Default values
        # tiles_url = 'http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png'
        tiles_url = 'https://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}'
        # tiles_attribution = '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        tiles_attribution = 'Esri, USGS | Esri, HERE | Esri, Garmin, FAO, NOAA'
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
        # TODO 1: Redirect to CDN
        quality = options.get('chart_options', {}).get('quality','4')
        if len(str(au)) > 2:
            cd_uf=str(au)[:2]
            res = 'municipio'
            state_geo = f'https://raw.githubusercontent.com/smartlab-br/geodata/master/geojson/br/{visao}/{res}/{cd_uf}_q{quality}.json'
        elif len(str(au)) == 2 and options.get('chart_options', {}).get('topology') == 'uf':
            state_geo = f'https://raw.githubusercontent.com/smartlab-br/geodata/master/geojson/br/uf_q{quality}.json'
        # Trocar por topojson dos estados no Brasil
        elif (res == visao):
            state_geo = f'https://raw.githubusercontent.com/smartlab-br/geodata/master/geojson/br/{visao}/{au}_q{quality}.json'
        else:
            state_geo = f'https://raw.githubusercontent.com/smartlab-br/geodata/master/geojson/br/{visao}/{res}/{au}_q{quality}.json' 
        # TODO 1 - Change the geo/topo json lookup address
        # state_geo = requests.get(state_geo).json()
        state_geo = requests.get('https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-29-mun.json').json()
        
        dataframe['str_id'] = dataframe[chart_options.get('id_field')].astype(str)
        dataframe['idx'] = dataframe[chart_options.get('id_field')]
        
        # Runs dataframe modifiers from viewconf
        dataframe = ViewConfReader().generate_columns(dataframe, options)

        dataframe = dataframe.set_index('idx')
        centroide = None  
        marker_tooltip = ''
        for each_au in state_geo.get('features'):
            # TODO 2 - Add a mechanism to know the identifying property in each geo/topo json
            # each_au.get('properties').update(json.loads(dataframe.loc[int(each_au.get('properties').get(chart_options.get('id_field')))].to_json()), headers=options.get('headers'))
            df_row = json.loads(dataframe.loc[int(each_au.get('properties').get("id"))].to_json())
            each_au.get('properties').update(df_row, headers=options.get('headers'))
            if str(each_au.get('properties', {}).get(chart_options.get('id_field'))) == str(au):
                centroide = each_au.get('properties', {}).get('centroide')
                if centroide:
                    centroide.reverse()
                marker_tooltip = "".join([f"<tr style='text-align: left;'><th style='padding: 4px; padding-right: 10px;'>{html.escape(hdr.get('text'))}</th><td style='padding: 4px;'>{html.escape(str(df_row[hdr.get('value')]))}</td></tr>" for hdr in options.get('headers')])
                marker_tooltip = f"<table>{marker_tooltip}</table>"
        state_geo = json.dumps(state_geo)
        
        # Creating map instance
        n = folium.Map(tiles=tiles_url, attr = tiles_attribution, control_scale = True)

        # Creating the choropleth layer
        color_scale = ViewConfReader.get_color_scale(
            options,
            dataframe[chart_options['value_field']].min(), 
            dataframe[chart_options['value_field']].max()
        )
        def get_color(feature):
            value = feature.get('properties',{}).get(chart_options['value_field'])
            if value is None:
                return '#8c8c8c' # MISSING -> gray
            else:
                return color_scale(value)

        chart = folium.GeoJson(
            data = state_geo,
            name = ViewConfReader.get_chart_title(options),
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

        n.get_root().header.add_child(folium.Element(style_statement))
        n.fit_bounds(n.get_bounds())
        return n
