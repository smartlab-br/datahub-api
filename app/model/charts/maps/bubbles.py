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
        chart_options['base_radius'] = chart_options.get('base_radius', self.BASE_RADIUS)
        chart_options['multiplier'] = chart_options.get('multiplier', self.RADIUS_MULTIPLIER)
        def get_circle_radius(row, **kwargs):
            chart_options = kwargs.get('chart_options')
            value = row[chart_options.get('value_field', 'api_calc_ln_norm_pos_part')]
            return chart_options.get('base_radius') + chart_options.get('multiplier') * value
        dataframe['radius'] = dataframe.apply(
            get_circle_radius,
            chart_options=chart_options,
            axis=1
        )

        grouped = dataframe.groupby(chart_options.get('layer_id', 'cd_indicador'))
        show = True # Shows only the first layer
        for group_id, group in grouped:
            # Get the color of the bubble according to layer definitions
            color = 'blue'
            for ind_index in range(len(chart_options.get('indicadores', []))):
                if chart_options.get('indicadores')[ind_index] == group_id:
                    color = chart_options.get('colorArray')[ind_index]
                    break

            if 'timeseries' not in chart_options:
                # Creating a layer for the group
                layer = FeatureGroup(
                    name=ViewConfReader.get_layers_names(options.get('headers')).get(group_id),
                    show=show
                )
                show = False

                # Generating circles
                for _row_index, row in group.iterrows():
                    CircleMarker(
                        location=[
                            row[chart_options.get('lat', 'latitude')],
                            row[chart_options.get('long', 'longitude')]
                        ],
                        radius=row['radius'],
                        popup=row['tooltip'],
                        color=color,
                        fill=True,
                        fill_color=color
                    ).add_to(layer)

                # Adding layer to map
                layer.add_to(result)
            else:
                features = []
                for _row_index, row in group.iterrows():
                    features.append({
                        'type': 'Feature',
                        'geometry': {
                            'type':'Point',
                            'coordinates':[
                                row[chart_options.get('long', 'longitude')],
                                row[chart_options.get('lat', 'latitude')]
                            ]
                        },
                        'properties': {
                            'time': pd.to_datetime(
                                row[chart_options.get('timeseries', 'nu_competencia')],
                                format='%Y'
                            ).__str__(),
                            'style': {'color' : color},
                            'icon': 'circle',
                            'iconstyle':{
                                'fillColor': color,
                                'fillOpacity': 0.8,
                                'stroke': 'true',
                                'radius': row['radius']
                            }
                        }
                    })

                TimestampedGeoJson(
                    features,
                    period='P1Y',
                    duration='P1Y',
                    date_options='YYYY',
                    transition_time=1000,
                    auto_play=True
                ).add_to(result)

                show = False

        result = self.add_au_marker(
            result, options.get('au'),
            dataframe=dataframe,
            options=options,
            chart_options=chart_options
        )
        result = self.post_adjustments(result, dataframe, chart_options)
        return result
