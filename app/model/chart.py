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
from service.charts.maps.choropleth import Choropleth
from service.charts.maps.heat import Heat
from service.charts.maps.cluster import Cluster
from service.charts.maps.bubbles import Bubbles

class Chart(BaseModel):
    ''' Model for fetching dinamic and static charts '''
    CHART_LIB_DEF = {
        'FOLIUM': ['MAP_TOPOJSON', 'MAP_HEAT', 'MAP_CLUSTER', 'MAP_BUBBLES']
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
            # TODO - [REMOVE] Testing heatmap with time series
            # struct['api']['template'] = "/te/indicadoresmunicipais?categorias=latitude,nu_competencia,longitude,cd_mun_ibge,nm_municipio,cd_indicador&valor=vl_indicador&agregacao=sum&filtros=nn-vl_indicador,and,in-cd_indicador-'te_rgt'-'te_nat'-'te_res',and,eq-cd_uf-{0}&calcs=ln_norm_pos_part"
            # struct['chart_options']['timeseries'] = 'nu_competencia'
            
            # TODO - [REMOVE] Testing bubbles with time series
            # struct['api']['template'] = "/te/indicadoresmunicipais?categorias=latitude,longitude,cd_mun_ibge,nm_municipio,nu_competencia,cd_indicador&valor=vl_indicador&agregacao=sum&filtros=nn-vl_indicador,and,in-cd_indicador-'te_rgt'-'te_nat'-'te_res',and,eq-cd_uf-{0}&calcs=ln_norm_pos_part"
            # struct['chart_options']['timeseries'] = 'nu_competencia'
            
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
            return Choropleth().draw(dataframe, options)
        if options.get('chart_type') == 'MAP_HEAT':
            return Heat().draw(dataframe, options)
        if options.get('chart_type') == 'MAP_CLUSTER':
            return Cluster().draw(dataframe, options)
        if options.get('chart_type') == 'MAP_BUBBLES':
            return Bubbles().draw(dataframe, options)
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
