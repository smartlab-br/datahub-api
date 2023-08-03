""" Model for fetching chart """
from folium.plugins import MarkerCluster
from model.charts.maps.base import BaseMap
from service.viewconf_reader import ViewConfReader


class Cluster(BaseMap):
    """ Heatmap building class """
    def draw(self):
        """ Gera um mapa de cluster a partir das opções enviadas """
        # http://localhost:5000/charts/cluster?from_viewconf=S&au=2927408&card_id=mapa_prev_estado_cluster&observatory=te&dimension=prevalencia&as_image=N
        chart_options = self.options.get('chart_options')
        # TODO - [REMOVE] Used just for debugging
        # options["headers"] = [
        #     {'text': 'nm_municipio', "value": 'nm_municipio'},

        #     {'text': 'te_rgt_agr_sum_vl_indicador', "value": 'te_rgt_agr_sum_vl_indicador'},
        #     {'text': 'te_rgt_api_calc_min_part', "value": 'te_rgt_api_calc_min_part'},
        #     {'text': 'te_rgt_api_calc_max_part', "value": 'te_rgt_api_calc_max_part'},
        #     {
        #         'text': 'te_rgt_api_calc_ln_norm_pos_part',
        #         "value": 'te_rgt_api_calc_ln_norm_pos_part'
        #     },

        #     {'text': 'te_res_agr_sum_vl_indicador', "value": 'te_res_agr_sum_vl_indicador'},
        #     {'text': 'te_res_api_calc_min_part', "value": 'te_res_api_calc_min_part'},
        #     {'text': 'te_res_api_calc_max_part', "value": 'te_res_api_calc_max_part'},
        #     {
        #         'text': 'te_res_api_calc_ln_norm_pos_part',
        #         "value": 'te_rgt_api_calc_ln_norm_pos_part'
        #     },

        #     {'text': 'te_nat_agr_sum_vl_indicador', "value": 'te_nat_agr_sum_vl_indicador'},
        #     {'text': 'te_nat_api_calc_min_part', "value": 'te_nat_api_calc_min_part'},
        #     {'text': 'te_nat_api_calc_max_part', "value": 'te_nat_api_calc_max_part'},
        #     {
        #         'text': 'te_nat_api_calc_ln_norm_pos_part',
        #         "value": 'te_nat_api_calc_ln_norm_pos_part'
        #     }
        # ]

        result = self.pre_draw(self.get_tooltip_data())

        grouped = self.dataframe.groupby(chart_options.get('layer_id', 'cd_indicador'))
        show = True # Shows only the first layer
        for group_id, group in grouped:
            chart = MarkerCluster(
                locations=group[self.get_location_columns()].values.tolist(),
                name=ViewConfReader.get_layers_names(self.options.get('headers')).get(group_id),
                show=show,
                popups=group['tooltip'].tolist()
            )

            show = False
            chart.add_to(result)

        result = self.add_au_marker(result, self.options.get('au'))

        return self.post_adjustments(result)
