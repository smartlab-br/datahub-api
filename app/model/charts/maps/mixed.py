''' Model for fetching chart '''
import folium
from model.charts.maps.base import BaseMap

class Mixed(BaseMap):
    """ Mixed map building class """
    def __init__(self, layers):
        self.layers = layers

    def draw(self, dataframe, options):
        """ Generates a base map and add layers according to config """
        # Creating map instance
        result = folium.Map(tiles=self.TILES_URL, attr=self.TILES_ATTRIBUTION, control_scale=True)

        # Generates layers
        for each_layer, each_df, each_option in zip(self.layers, dataframe, options):
            analysis_unit = each_option.get('au')

            if each_option.get('chart_type') == 'MAP_TOPOJSON':
                # Gets the geometry
                each_df = each_layer.prepare_dataframe(each_df, each_option.get('chart_options'))
                # Join dataframe and state_geo
                (state_geo, centroid) = each_layer.join_df_geo(
                    each_df,
                    each_layer.get_geometry(each_option, analysis_unit),
                    each_option
                )
                # Generating choropleth layer
                each_layer.layer_gen(each_df, each_option.get('chart_options'), state_geo, each_option).add_to(result)
            elif each_option.get('chart_type') == 'MAP_BUBBLES':
                # Adds tooltip data
                each_df = each_layer.prepare_dataframe(
                    each_df,
                    each_option.get('chart_options'),
                    self.get_tooltip_data(each_df, each_option.get('chart_options'), each_option)
                )
                # Get grouped dataframe
                grouped = each_df.groupby(each_option.get('layer_id', 'cd_indicador'))
                for group_id, group in grouped:
                    each_layer.layer_gen(each_option.get('chart_options'), group, group_id, True, each_option).add_to(result)

        folium.LayerControl().add_to(result)

        result.get_root().header.add_child(folium.Element(self.STYLE_STATEMENT))

        # Getting bounds from topojson
        lower_left = state_geo.get('bbox')[:2]
        lower_left.reverse()
        upper_right = state_geo.get('bbox')[2:]
        upper_right.reverse()

        # Zooming to bounds
        result.fit_bounds([lower_left, upper_right])

        return result
