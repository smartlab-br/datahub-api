''' Model for fetching chart '''
import folium
from model.charts.maps.base import BaseMap

class Mixed(BaseMap):
    """ Mixed map building class """
    def draw(self, dataframe, options):
        """ Generates a base map and add layers according to config """
        # http://localhost:5000/charts/choropleth?from_viewconf=S&au=2927408&card_id=mapa_pib_brasil&dimension=socialeconomico&as_image=S
        analysis_unit = options.get('au')

        # Creating map instance
        result = folium.Map(tiles=self.TILES_URL, attr=self.TILES_ATTRIBUTION, control_scale=True)

        # Generates layers
        for each_df, each_option in zip(dataframe, options):
            if each_option.get('chart_type') == 'MAP_TOPOJSON':
                # Join dataframe and state_geo
                (state_geo, centroid) = self.join_df_geo(
                    dataframe,
                    self.get_geometry(options, analysis_unit),
                    options
                )
                # Generating choropleth layer
                self.layer_gen(each_df, each_option, state_geo, each_option).add_to(result)
            elif each_option.get('chart_type') == 'MAP_BUBBLES':
                grouped = dataframe.groupby(each_option.get('layer_id', 'cd_indicador'))
                for group_id, group in grouped:
                    self.layer_gen(each_option, group, group_id, True, options).add_to(result)

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
