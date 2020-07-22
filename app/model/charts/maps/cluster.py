''' Model for fetching chart '''
import folium
from folium.plugins import MarkerCluster
from model.charts.maps.base import BaseMap
from service.viewconf_reader import ViewConfReader

class Cluster(BaseMap):
    ''' Heatmap building class '''
    def draw(self, dataframe, options):
        ''' Gera um mapa de cluster a partir das opções enviadas '''
        # http://localhost:5000/charts/cluster?from_viewconf=S&au=2927408&card_id=mapa_prev_estado_cluster&observatory=te&dimension=prevalencia&as_image=N
        chart_options = options.get('chart_options')
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

        (dataframe, result, options) = self.pre_draw(
            dataframe, chart_options, options,
            self.get_tooltip_data(dataframe, chart_options, options)
        )

        grouped = dataframe.groupby(chart_options.get('layer_id', 'cd_indicador'))
        show = True # Shows only the first layer
        for group_id, group in grouped:
            chart = MarkerCluster(
                locations=group[self.get_location_columns(chart_options)].values.tolist(),
                name=ViewConfReader.get_layers_names(options.get('headers')).get(group_id),
                show=show,
                popups=group['tooltip'].tolist()
            )

            show = False
            chart.add_to(result)

        result = self.add_au_marker(
            result, options.get('au'),
            dataframe=dataframe,
            options=options,
            chart_options=chart_options
        )
        result = self.post_adjustments(result, dataframe, chart_options)
        return result
