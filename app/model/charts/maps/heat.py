''' Model for fetching chart '''
import folium
import numpy as np
from folium.plugins import HeatMap, HeatMapWithTime
from model.charts.maps.base import BaseMap
from service.viewconf_reader import ViewConfReader

class Heat(BaseMap):
    ''' Heatmap building class '''
    def draw(self, dataframe, options):
        ''' Gera um mapa de calor a partir das opções enviadas '''
        # http://localhost:5000/charts/choropleth?from_viewconf=S&au=2927408&card_id=mapa_pib_brasil&dimension=socialeconomico&as_image=S
        analysis_unit = options.get('au')
        chart_options = options.get('chart_options')

        (dataframe, result, options) = self.pre_draw(
            dataframe, chart_options, options,
            self.get_tooltip_data(dataframe, chart_options, options)
        )

        centroide = None
        cols = [chart_options.get('lat', 'lat'), chart_options.get('long', 'long')]
        if 'value_field' in chart_options:
            cols.append(chart_options.get('value_field'))

        # Get group names from headers
        group_names = ViewConfReader.get_layers_names(options.get('headers'))
        grouped = dataframe.groupby(chart_options.get('layer_id', 'cd_indicador'))
        show = True # Shows only the first
        for group_id, group in grouped:
            if 'timeseries' not in chart_options:
                chart = HeatMap(
                    group[cols].values.tolist(),
                    name=group_names.get(group_id),
                    show=show
                )
            else:
                t_grouped = group.groupby(chart_options.get('timeseries'))
                t_data = []
                t_index = []
                for t_group_id, t_group in t_grouped:
                    t_data.append(t_group[cols].values.tolist())
                    t_index.append(t_group_id)
                chart = HeatMapWithTime(
                    t_data,
                    index=t_index,
                    auto_play=True,
                    name=group_names.get(group_id),
                    show=show
                )
            chart.add_to(result)
            show = False

        # Adding marker to current analysis unit
        if np.issubdtype(dataframe.index.dtype, np.number):
            analysis_unit = int(analysis_unit)

        au_row = dataframe.loc[analysis_unit].pivot_table(
            index=[
                chart_options.get('id_field', 'cd_mun_ibge'),
                chart_options.get('name_field', 'nm_municipio'),
                chart_options.get('lat', 'latitude'),
                chart_options.get('long', 'longitude')
            ],
            columns='cd_indicador',
            values=chart_options.get('value_field', 'vl_indicador')
        ).reset_index().iloc[0]

        if chart_options.get('lat', 'latitude') in list(dataframe.columns):
            centroide = [
                au_row[chart_options.get('lat', 'latitude')],
                au_row[chart_options.get('long', 'longitude')]
            ]

        if centroide:
            marker_layer = folium.map.FeatureGroup(
                name=self.get_au_title(au_row, options.get('headers'))
            )
            folium.map.Marker(
                centroide,
                tooltip=self.tooltip_gen(au_row, headers=options.get('headers')),
                icon=folium.Icon(color=ViewConfReader.get_marker_color(options))
            ).add_to(marker_layer)
            marker_layer.add_to(result)

        return self.post_adjustments(result, dataframe, chart_options)

    @staticmethod
    def tooltip_gen(row, **kwargs):
        pass
