''' Model for fetching chart '''
import pandas as pd
from folium import CircleMarker
from folium.plugins import TimestampedGeoJson
from folium.map import FeatureGroup
from model.charts.maps.base import BaseMap
from service.viewconf_reader import ViewConfReader

class Bubbles(BaseMap):
    ''' Heatmap building class '''
    BASE_RADIUS = 1
    RADIUS_MULTIPLIER = 50

    def draw(self, dataframe, options):
        ''' Gera um mapa topojson a partir das opções enviadas '''
        # http://localhost:5000/charts/cluster?from_viewconf=S&au=2927408&card_id=mapa_prev_estado&observatory=te&dimension=prevalencia&as_image=N
        chart_options = options.get('chart_options')
        (dataframe, result, options) = self.pre_draw(
            dataframe, chart_options, options,
            self.get_tooltip_data(dataframe, chart_options, options)
        )

        # Adding circle radius to dataset
        dataframe['radius'] = self.assess_radius(dataframe, chart_options)

        grouped = dataframe.groupby(chart_options.get('layer_id', 'cd_indicador'))
        show = True # Shows only the first layer
        for group_id, group in grouped:
            # Get the color of the bubble according to layer definitions
            self.layer_gen(chart_options, group, group_id, show, options).add_to(result)
            show = False

        result = self.add_au_marker(
            result, options.get('au'),
            dataframe=dataframe,
            options=options,
            chart_options=chart_options
        )
        result = self.post_adjustments(result, dataframe, chart_options)
        return result

    def assess_radius(self, dataframe, chart_options):
        """ Generates a Series with bubbles radius for row in dataframe """
        chart_options['base_radius'] = chart_options.get('base_radius', self.BASE_RADIUS)
        chart_options['multiplier'] = chart_options.get('multiplier', self.RADIUS_MULTIPLIER)

        def get_circle_radius(row, **kwargs):
            chart_opts = kwargs.get('chart_options')
            value = row[chart_opts.get('value_field', 'api_calc_ln_norm_pos_part')]
            return chart_opts.get('base_radius') + chart_opts.get('multiplier') * value

        return dataframe.apply(get_circle_radius, chart_options=chart_options, axis=1)

    def layer_gen(self, chart_options, group, group_id, show, options):
        """ Generates a bubbles layer """
        # Get the color of the bubble according to layer definitions
        color = 'blue'
        for ind_index in range(len(chart_options.get('indicadores', []))):
            if chart_options.get('indicadores')[ind_index] == group_id:
                color = chart_options.get('colorArray')[ind_index]
                break

        # Adding circle radius to group, if it's not present in dataframe group
        if 'radius' not in group.columns:
            group['radius'] = self.assess_radius(group, chart_options)

        if 'timeseries' not in chart_options:
            # Creating a layer for the group
            layer = FeatureGroup(
                name=ViewConfReader.get_layers_names(options.get('headers')).get(group_id),
                show=show
            )

            # Check if popup data is present
            has_tooltip = 'tooltip' in group.columns

            # Generating circles
            for _row_index, row in group.iterrows():
                tooltip_data = None
                if has_tooltip:
                    tooltip_data = row['tooltip']

                CircleMarker(
                    location=[
                        row[chart_options.get('lat', 'latitude')],
                        row[chart_options.get('long', 'longitude')]
                    ],
                    radius=row['radius'],
                    popup=tooltip_data,
                    color=color,
                    fill=True,
                    fill_color=color
                ).add_to(layer)

            # Adding layer to map
            return layer
        else:
            features = []
            for _row_index, row in group.iterrows():
                features.append({
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [
                            row[chart_options.get('long', 'longitude')],
                            row[chart_options.get('lat', 'latitude')]
                        ]
                    },
                    'properties': {
                        'time': pd.to_datetime(
                            row[chart_options.get('timeseries', 'nu_competencia')],
                            format='%Y'
                        ).__str__(),
                        'style': {'color': color},
                        'icon': 'circle',
                        'iconstyle': {
                            'fillColor': color,
                            'fillOpacity': 0.8,
                            'stroke': 'true',
                            'radius': row['radius']
                        }
                    }
                })

            return TimestampedGeoJson(
                features,
                period='P1Y',
                duration='P1Y',
                date_options='YYYY',
                transition_time=1000,
                auto_play=True
            )
