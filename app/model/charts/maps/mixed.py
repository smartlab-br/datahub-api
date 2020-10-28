''' Model for fetching chart '''
import folium
from model.charts.maps.base import BaseMap

class Mixed(BaseMap):
    """ Mixed map building class """
    def __init__(self, layers):
        super().__init__(None, None)  # Blocks instantiation of dataframes and options
        self.layers = layers

    def draw(self):
        """ Generates a base map and add layers according to config """
        # Creating map instance
        result = folium.Map(tiles=self.TILES_URL, attr=self.TILES_ATTRIBUTION, control_scale=True)

        # Generates layers
        for layer in self.layers:
            analysis_unit = layer.options.get('au')

            if layer.options.get('chart_type') == 'MAP_TOPOJSON':
                layer.prepare_dataframe()
                # Join dataframe and state_geo
                (state_geo, centroid) = layer.join_df_geo(layer.get_geometry(analysis_unit))
                # Generating choropleth layer
                layer.layer_gen(state_geo).add_to(result)
            elif layer.options.get('chart_type') == 'MAP_BUBBLES':
                layer.prepare_dataframe(layer.get_tooltip_data())
                # Get grouped dataframe
                grouped = layer.dataframe.groupby(layer.options.get('layer_id', 'cd_indicador'))
                for group_id, group in grouped:
                    layer.layer_gen(group, group_id, True).add_to(result)

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
