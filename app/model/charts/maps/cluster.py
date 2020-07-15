''' Model for fetching chart '''
import folium
import numpy as np
import pandas as pd
from model.charts.maps.base import BaseMap
from folium.plugins import MarkerCluster
from service.viewconf_reader import ViewConfReader

class Cluster(BaseMap):
    ''' Heatmap building class '''
    def draw(self, dataframe, options):
        ''' Gera um mapa de cluster a partir das opções enviadas '''
        # http://localhost:5000/charts/cluster?from_viewconf=S&au=2927408&card_id=mapa_prev_estado_cluster&observatory=te&dimension=prevalencia&as_image=N
        chart_options = options.get('chart_options')
        dataframe = self.prepare_dataframe(dataframe, chart_options)

        # Creating map instance
        n = folium.Map(tiles=self.TILES_URL, attr = self.TILES_ATTRIBUTION, control_scale = True)
        
        options['headers'] = self.get_headers(chart_options, options)
        
        # Adding tooltips to detailed dataframe
        dataframe = pd.merge(
            dataframe,
            self.get_tooltip_data(dataframe, chart_options, options),
            left_on = chart_options.get('id_field', 'cd_mun_ibge'),
            right_on = chart_options.get('id_field', 'cd_mun_ibge'),
            how = "left"
        )
        dataframe['idx'] = dataframe[chart_options.get('id_field', 'cd_mun_ibge')]
        dataframe = dataframe.set_index('idx')
        
        grouped = dataframe.groupby(chart_options.get('layer_id','cd_indicador'))
        show = True # Shows only the first layer
        for group_id, group in grouped:
            chart = MarkerCluster(
                locations = group[self.get_location_columns(chart_options)].values.tolist(),
                name = {hdr.get('layer_id'): hdr.get('text') for hdr in options.get('headers') if hdr.get('layer_id')}.get(group_id),
                show = show,
                popups = group['tooltip'].tolist()
            )

            show = False
            chart.add_to(n)

        n = self.add_au_marker(n, dataframe, options.get('au'), options, chart_options)    
        n = self.post_adjustments(n, dataframe, chart_options)
        return n
