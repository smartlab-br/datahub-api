''' Model for fetching chart '''
import folium
import numpy as np
from model.charts.maps.base import BaseMap
from folium.plugins import HeatMap, HeatMapWithTime
from service.viewconf_reader import ViewConfReader

class Heat(BaseMap):
    ''' Heatmap building class '''
    def draw(self, dataframe, options):
        ''' Gera um mapa de calor a partir das opções enviadas '''
        # http://localhost:5000/charts/choropleth?from_viewconf=S&au=2927408&card_id=mapa_pib_brasil&dimension=socialeconomico&as_image=S
        visao = options.get('visao', 'uf')

        au = options.get('au')
        chart_options = options.get('chart_options')

        dataframe['str_id'] = dataframe[chart_options.get('id_field', 'cd_mun_ibge')].astype(str)
        dataframe['idx'] = dataframe[chart_options.get('id_field', 'cd_mun_ibge')]
        
        # Runs dataframe modifiers from viewconf
        dataframe = ViewConfReader().generate_columns(dataframe, options)

        dataframe = dataframe.set_index('idx')
        centroide = None  
        marker_tooltip = ''
        
        # Creating map instance
        n = folium.Map(tiles=self.TILES_URL, attr = self.TILES_ATTRIBUTION, control_scale = True)

        cols = [chart_options.get('lat','lat'), chart_options.get('long','long')]
        if 'value_field' in chart_options:
            cols.append(chart_options.get('value_field'))

        if 'headers' not in options:
            options['headers'] = ViewConfReader.get_headers_from_options_descriptor(
                options.get('description'),
                [{
                    'text': 'Analysis Unit',
                    'value': chart_options.get('name_field', 'nm_municipio')
                }]
            )
            
        # Get group names from headers
        group_names = { hdr.get('layer_id'): hdr.get('text') for hdr in options.get('headers') if hdr.get('layer_id') }

        grouped = dataframe.groupby(chart_options.get('layer_id','cd_indicador'))
        show = True # Shows only the first
        for group_id, group in grouped:
            if 'timeseries' not in chart_options:
                chart = HeatMap(
                    group[cols].values.tolist(),
                    name = group_names.get(group_id),
                    show = show
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
                    index = t_index,
                    auto_play=True,
                    name = group_names.get(group_id),
                    show = show
                )
            chart.add_to(n)
            show = False
            
        # Adding marker to current analysis unit
        if np.issubdtype(dataframe.index.dtype, np.number):
            au = int(au)

        au_row = dataframe.loc[au].pivot_table(
            index=[chart_options.get('id_field','cd_mun_ibge'), chart_options.get('name_field', 'nm_municipio'), chart_options.get('lat','latitude'), chart_options.get('long','longitude')],
            columns='cd_indicador',
            values=chart_options.get('value_field','vl_indicador')
        ).reset_index().iloc[0]
        
        au_title = 'Analysis Unit'
        if len(options.get('headers', [])) > 0:
            au_title = au_row[options.get('headers', [])[0]['value']]

        if chart_options.get('lat','latitude') in list(dataframe.columns):
            centroide = [au_row[chart_options.get('lat','latitude')], au_row[chart_options.get('long','longitude')]]
        
        if 'headers' in options:
            marker_tooltip = "".join([f"<tr style='text-align: left;'><th style='padding: 4px; padding-right: 10px;'>{hdr.get('text').encode('ascii', 'xmlcharrefreplace').decode()}</th><td style='padding: 4px;'>{str(au_row[hdr.get('value')]).encode('ascii', 'xmlcharrefreplace').decode()}</td></tr>" for hdr in options.get('headers')])
            marker_tooltip = f"<table>{marker_tooltip}</table>"
        else:
            marker_tooltip = "Tooltip!"

        if centroide:
            marker_layer = folium.map.FeatureGroup(name = au_title)
            folium.map.Marker(
                centroide,
                tooltip=marker_tooltip,
                icon=folium.Icon(color=ViewConfReader.get_marker_color(options))
            ).add_to(marker_layer)
            marker_layer.add_to(n)
        
        folium.LayerControl().add_to(n)

        n.get_root().header.add_child(folium.Element(self.STYLE_STATEMENT))

        # Getting bounds from dataframe
        n.fit_bounds([
            [
                dataframe[chart_options.get('lat','latitude')].min(),
                dataframe[chart_options.get('long','longitude')].min()
            ],
            [
                dataframe[chart_options.get('lat','latitude')].max(),
                dataframe[chart_options.get('long','longitude')].max()
            ]
        ])

        return n
