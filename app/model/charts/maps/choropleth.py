""" Model for fetching chart """
import json
import numpy as np
import folium
import requests
from service.viewconf_reader import ViewConfReader
from model.charts.maps.base import BaseMap


class Choropleth(BaseMap):
    """ Choropleth building class """
    BASE_TOPOJSON_REPO = 'https://raw.githubusercontent.com/smartlab-br/geodata/master/topojson/br'

    def draw(self):
        """ Gera um mapa topojson a partir das opções enviadas """
        # http://localhost:5000/charts/choropleth?from_viewconf=S&au=2927408&card_id=mapa_pib_brasil&dimension=socialeconomico&as_image=S
        analysis_unit = self.options.get('au')

        # Gets the geometry
        self.prepare_dataframe()

        # Join dataframe and state_geo
        (state_geo, centroid) = self.join_df_geo(self.get_geometry(analysis_unit))

        # Creating map instance
        result = folium.Map(tiles=self.TILES_URL, attr=self.TILES_ATTRIBUTION, control_scale=True)

        # Generating choropleth layer
        chart = self.layer_gen(state_geo)

        # Adding marker to current analysis unit
        if np.issubdtype(self.dataframe.index.dtype, np.number):
            analysis_unit = int(analysis_unit)
        au_row = self.dataframe.loc[analysis_unit]

        if 'latitude' in list(self.dataframe.columns):
            centroid = [au_row['latitude'], au_row['longitude']]

        if centroid:
            marker_layer = folium.map.FeatureGroup(
                name=self.get_au_title(au_row, self.options.get('headers'))
            )
            folium.map.Marker(
                centroid,
                tooltip=self.tooltip_gen(au_row, self.options.get('headers')),
                icon=folium.Icon(color=ViewConfReader.get_marker_color(self.options))
            ).add_to(marker_layer)
            marker_layer.add_to(result)

        chart.add_to(result)
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

    @staticmethod
    def get_feature_color(color_scale, feature, value_field):
        if feature is None:
            return '#8c8c8c'  # MISSING -> gray
        value = None
        if value_field in feature.get('properties', {}):
            value = feature.get('properties', {}).get(value_field)
        if value is None:
            return '#8c8c8c'  # MISSING -> gray
        return color_scale(value)

    def get_geometry(self, analysis_unit):
        """ Gets the topojson from external resource """
        return requests.get(self.get_geometry_loc(analysis_unit)).json()

    def get_geometry_loc(self, analysis_unit):
        """ Gets the topojson location """
        if self.options is None:
            visao = 'uf'
            quality = 1
            res = 'municipio'
        else:
            visao = self.options.get('visao', 'uf')
            quality = self.options.get('chart_options', {}).get('quality', '1')
            res = self.options.get('chart_options', {}).get('resolution', 'municipio')
            topology = self.options.get('chart_options', {}).get('topology')
        if analysis_unit is None or (len(str(analysis_unit)) == 2 and topology == 'uf'):
            return f'{self.BASE_TOPOJSON_REPO}/uf_q{quality}.json'
        if len(str(analysis_unit)) == 7 and visao == 'uf':
            cd_uf = str(analysis_unit)[:2]
            return f'{self.BASE_TOPOJSON_REPO}/{visao}/{res}/{cd_uf}_q{quality}.json'
        if res == visao:
            return f'{self.BASE_TOPOJSON_REPO}/{visao}/{analysis_unit}_q{quality}.json'
        return f'{self.BASE_TOPOJSON_REPO}/{visao}/{res}/{analysis_unit}_q{quality}.json'

    def layer_gen(self, state_geo):
        """ Generates a choropleth layer """
        chart_options = self.options.get('chart_options', {})
        # Creating the choropleth layer
        color_scale = ViewConfReader.get_color_scale(
            self.options,
            self.dataframe[chart_options.get('value_field', 'vl_indicador')].min(),
            self.dataframe[chart_options.get('value_field', 'vl_indicador')].max()
        )

        color_function = self.get_feature_color
        chart = folium.TopoJson(
            state_geo,
            'objects.data',
            name=ViewConfReader.get_chart_title(self.options),
            style_function=lambda feature: {
                'fillColor': color_function(color_scale, feature, chart_options.get('value_field')),
                'fillOpacity': 0.8,
                'color': 'black',
                'stroke': 'black',
                'lineOpacity': 0.2,
                'weight': 0.2,
            }
        )

        # Adding tooltip to choropleth
        folium.features.GeoJsonTooltip(
            fields=[hdr.get('value') for hdr in self.options.get('headers')],
            aliases=[hdr.get('text') for hdr in self.options.get('headers')],
            localize=True,
            sticky=False,
            labels=True
        ).add_to(chart)

        return chart

    def join_df_geo(self, state_geo):
        """ Joins dataframe into geo data """
        centroid = None
        # for each_au in state_geo.get('features'):
        for each_au in state_geo.get('objects', {}).get('data', {}).get('geometries', []):
            # During topo conversion, all ID will be named smartlab_geo_id and
            # all NAME will be in an attribute called smartlab_geo_name.
            try:
                df_row = self.dataframe.set_index('idx').loc[int(each_au.get('properties').get("smartlab_geo_id"))]
                each_au.get('properties').update(
                    json.loads(df_row.to_json()),
                    headers=self.options.get('headers')
                )
            except KeyError:
                df_row = {hdr.get('value'): 'N/A' for hdr in self.options.get('headers')}
                df_row[self.options.get('headers')[0].get('value')] = each_au.get(
                    'properties'
                ).get('smartlab_geo_name')
                each_au.get('properties').update(
                    json.loads(json.dumps(df_row)),
                    headers=self.options.get('headers')
                )
            if str(each_au.get('properties', {}).get(self.options.get('chart_options', {}).get('id_field'))) == str(self.options.get('au')):
                centroid = each_au.get('properties', {}).get('centroide')
                if centroid:
                    centroid.reverse()
        return state_geo, centroid
