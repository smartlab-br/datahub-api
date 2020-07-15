''' Model for fetching chart '''
import folium
import pandas as pd
from model.charts.maps.base import BaseMap
from folium.plugins import MarkerCluster

class Cluster(BaseMap):
    ''' Heatmap building class '''
    def draw(self, dataframe, options):
        ''' Gera um mapa de cluster a partir das opções enviadas '''
        # http://localhost:5000/charts/cluster?from_viewconf=S&au=2927408&card_id=mapa_prev_estado_cluster&observatory=te&dimension=prevalencia&as_image=N
        chart_options = options.get('chart_options')
        dataframe = self.prepare_dataframe(dataframe, chart_options)

        # Creating map instance
        result = folium.Map(tiles=self.TILES_URL, attr=self.TILES_ATTRIBUTION, control_scale=True)
        
        options['headers'] = self.get_headers(chart_options, options)

        # TODO - [REMOVE] Used just for debugging
        # options["headers"] = [
        #     {'text': 'nm_municipio', "value": 'nm_municipio'},

        #     {'text': 'te_rgt_agr_sum_vl_indicador', "value": 'te_rgt_agr_sum_vl_indicador'},
        #     {'text': 'te_rgt_api_calc_min_part', "value": 'te_rgt_api_calc_min_part'},
        #     {'text': 'te_rgt_api_calc_max_part', "value": 'te_rgt_api_calc_max_part'},
        #     {'text': 'te_rgt_api_calc_ln_norm_pos_part', "value": 'te_rgt_api_calc_ln_norm_pos_part'},
            
        #     {'text': 'te_res_agr_sum_vl_indicador', "value": 'te_res_agr_sum_vl_indicador'},
        #     {'text': 'te_res_api_calc_min_part', "value": 'te_res_api_calc_min_part'},
        #     {'text': 'te_res_api_calc_max_part', "value": 'te_res_api_calc_max_part'},
        #     {'text': 'te_res_api_calc_ln_norm_pos_part', "value": 'te_rgt_api_calc_ln_norm_pos_part'},
            
        #     {'text': 'te_nat_agr_sum_vl_indicador', "value": 'te_nat_agr_sum_vl_indicador'},
        #     {'text': 'te_nat_api_calc_min_part', "value": 'te_nat_api_calc_min_part'},
        #     {'text': 'te_nat_api_calc_max_part', "value": 'te_nat_api_calc_max_part'},
        #     {'text': 'te_nat_api_calc_ln_norm_pos_part', "value": 'te_nat_api_calc_ln_norm_pos_part'}
        # ]

        # Adding tooltips to detailed dataframe
        dataframe = pd.merge(
            dataframe,
            self.get_tooltip_data(dataframe, chart_options, options),
            left_on=chart_options.get('id_field', 'cd_mun_ibge'),
            right_on=chart_options.get('id_field', 'cd_mun_ibge'),
            how="left"
        )
        dataframe['idx'] = dataframe[chart_options.get('id_field', 'cd_mun_ibge')]
        dataframe = dataframe.set_index('idx')

        grouped = dataframe.groupby(chart_options.get('layer_id', 'cd_indicador'))
        show = True # Shows only the first layer
        for group_id, group in grouped:
            chart = MarkerCluster(
                locations=group[self.get_location_columns(chart_options)].values.tolist(),
                name={hdr.get('layer_id'): hdr.get('text') for hdr in options.get('headers') if hdr.get('layer_id')}.get(group_id),
                show=show,
                popups=group['tooltip'].tolist()
            )

            show = False
            chart.add_to(result)

        result = self.add_au_marker(result, dataframe, options.get('au'), options, chart_options)
        result = self.post_adjustments(result, dataframe, chart_options)
        return result
