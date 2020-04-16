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
# Novos
# FIREFOX-ESR tem que estar no PATH
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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
            struct = ViewConfReader.get_card_descriptor(
                options.get('language', 'br'),
                options.get('observatory', 'td'),
                options.get('scope', 'municipio'),
                options.get('dimension'),
                options.get('card_id')
            )
            options = {**options, **ViewConfReader.api_to_options(struct.get('api'), {**options, **added_options}), **struct}

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
            </style>"

        au = options.get('au')
        chart_options = options.get('chart_options')

        # TODO 1 - Fazer funcionar com o topojson
        if len(str(au)) > 2 or (len(str(au)) == 2 and visao == 'uf'):
            cd_uf=str(au)[:2]
            state_geo = f'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-{cd_uf}-mun.json'
            # state_geo = f'./topojson/municipio/uf/{uf}.json'
        else:
            # Trocar por topojson dos estados no Brasil
            state_geo = f'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-29-mun.json'
        state_geo = requests.get(state_geo).json()

        dataframe['str_id'] = dataframe[chart_options.get('id_field')].astype(str)
        dataframe['idx'] = dataframe[chart_options.get('id_field')]

        # Runs dataframe modifiers from viewconf
        dataframe = ViewConfReader().generate_columns(dataframe, options)

        dataframe = dataframe.set_index('idx')    
        for each_au in state_geo.get('features'):
            each_au.get('properties').update(json.loads(dataframe.loc[int(each_au.get('properties').get('id'))].to_json()), headers=options.get('headers'))
        state_geo = json.dumps(state_geo)

        # Creating map instance
        n = folium.Map(tiles=tiles_url, attr = tiles_attribution, control_scale = True)

        # TODO 2 - Ajustar cores para a escala (linear, não em bins - tentar remover extremos, passando um array de cores HEX)
        # Creating the choropleth layer
        chart = folium.Choropleth(
            geo_data=state_geo,
            name='choropleth',
            data=dataframe,
            columns=['str_id', chart_options['value_field']],
            key_on='feature.properties.id',
            fill_color='Blues',
            fill_opacity=0.7,
            line_opacity=0.2,
            # bins=list(dataframe[chart_options['value_field']].quantile([0, 0.11, 0.22, 0.33, 0.44, 0.55, 0.66, 0.77, 0.88, 1])),
            highlight = True
        )

        # Adding tooltip to choropleth
        folium.features.GeoJsonTooltip(
            fields = [hdr.get('value') for hdr in options.get('headers')],
            aliases = [hdr.get('text') for hdr in options.get('headers')],
            localize=True,
            sticky=False,
            labels=True
        ).add_to(chart.geojson)

        # Adding marker to current analysis unit
        if np.issubdtype(dataframe.index.dtype, np.number):
            au = int(au)
        au_row = dataframe.loc[au]
        au_title = 'Analysis Unit'
        if len(options.get('headers', [])) > 0:
            au_title = au_row[options.get('headers', [])[0]['value']]
        marker_layer = folium.map.FeatureGroup(name = au_title)
        folium.map.Marker(
            [au_row['latitude'], au_row['longitude']],
            icon=folium.Icon(color='red') # TODO 4 - create function to find contrasting color.
        ).add_to(marker_layer)

        # Adding layers to map
        marker_layer.add_to(n)
        chart.add_to(n)
        folium.LayerControl().add_to(n)

        n.get_root().header.add_child(folium.Element(style_statement))
        n.fit_bounds(n.get_bounds())
        return n
