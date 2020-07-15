''' Model for fetching chart '''
import folium
import numpy as np
import pandas as pd
from model.charts.maps.base import BaseMap
from folium import CircleMarker
from folium.plugins import TimestampedGeoJson
from folium.map import FeatureGroup
from service.viewconf_reader import ViewConfReader

class Bubbles(BaseMap):
    ''' Heatmap building class '''
    BASE_RADIUS = 1
    RADIUS_MULTIPLIER = 50

    def draw(self, dataframe, options):
        ''' Gera um mapa topojson a partir das opções enviadas '''
        # http://localhost:5000/charts/cluster?from_viewconf=S&au=2927408&card_id=mapa_prev_estado&observatory=te&dimension=prevalencia&as_image=N
        # Check testing options.headers below!!!!
        au = options.get('au')
        chart_options = options.get('chart_options')

        dataframe['str_id'] = dataframe[chart_options.get('id_field', 'cd_mun_ibge')].astype(str)
        dataframe['idx'] = dataframe[chart_options.get('id_field', 'cd_mun_ibge')]
        
        # Runs dataframe modifiers from viewconf
        # dataframe = ViewConfReader().generate_columns(dataframe, options)

        dataframe = dataframe.set_index('idx')
        centroide = None  
        
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
        
        # Tooltip gen function
        # TODO - [REMOVE] Used just for debugging
        # options["headers"] = [
        #     {'text': 'nm_municipio', "value": 'nm_municipio'},

        #     {'text': 'te_rgt_agr_sum_vl_indicador', "layer_id": "te_rgt", "value": 'te_rgt_agr_sum_vl_indicador'},
        #     {'text': 'te_rgt_api_calc_min_part', "value": 'te_rgt_api_calc_min_part'},
        #     {'text': 'te_rgt_api_calc_max_part', "value": 'te_rgt_api_calc_max_part'},
        #     {'text': 'te_rgt_api_calc_ln_norm_pos_part', "value": 'te_rgt_api_calc_ln_norm_pos_part'},
            
        #     {'text': 'te_res_agr_sum_vl_indicador', "layer_id": "te_res", "value": 'te_res_agr_sum_vl_indicador'},
        #     {'text': 'te_res_api_calc_min_part', "value": 'te_res_api_calc_min_part'},
        #     {'text': 'te_res_api_calc_max_part', "value": 'te_res_api_calc_max_part'},
        #     {'text': 'te_res_api_calc_ln_norm_pos_part', "value": 'te_rgt_api_calc_ln_norm_pos_part'},
            
        #     {'text': 'te_nat_agr_sum_vl_indicador', "layer_id": "te_nat", "value": 'te_nat_agr_sum_vl_indicador'},
        #     {'text': 'te_nat_api_calc_min_part', "value": 'te_nat_api_calc_min_part'},
        #     {'text': 'te_nat_api_calc_max_part', "value": 'te_nat_api_calc_max_part'},
        #     {'text': 'te_nat_api_calc_ln_norm_pos_part', "value": 'te_nat_api_calc_ln_norm_pos_part'}
        # ]

        # Get group names from headers
        group_names = { hdr.get('layer_id'): hdr.get('text') for hdr in options.get('headers') if hdr.get('layer_id') }
        
        # Adding circle radius to dataset
        chart_options['base_radius'] = chart_options.get('base_radius', self.BASE_RADIUS)
        chart_options['multiplier'] = chart_options.get('multiplier', self.RADIUS_MULTIPLIER)
        def get_circle_radius(row, **kwargs):
            return chart_options.get('base_radius') + chart_options.get('multiplier') * row[chart_options.get('value_field','api_calc_ln_norm_pos_part')]
        dataframe['radius'] = dataframe.apply(
            get_circle_radius,
            chart_options = chart_options,
            axis=1
        )

        # Get pivoted dataframe for tooltip list creation
        df_tooltip = dataframe.copy().pivot_table(
            index=[chart_options.get('id_field','cd_mun_ibge'), chart_options.get('name_field', 'nm_municipio'), chart_options.get('lat','latitude'), chart_options.get('long','longitude')],
            columns='cd_indicador',
            fill_value=0
        )
        df_tooltip.columns = ['_'.join(reversed(col)).strip() for col in df_tooltip.columns.values]
        df_tooltip = df_tooltip.reset_index()
        
        # Adding tooltips to dataframe
        def tooltip_gen(au_row, **kwargs):
            if 'headers' in options:
                marker_tooltip = "".join([f"<tr style='text-align: left;'><th style='padding: 4px; padding-right: 10px;'>{hdr.get('text').encode('ascii', 'xmlcharrefreplace').decode()}</th><td style='padding: 4px;'>{str(au_row[hdr.get('value')]).encode('ascii', 'xmlcharrefreplace').decode()}</td></tr>" for hdr in kwargs.get('headers')])
                return f"<table>{marker_tooltip}</table>"
            return "Tooltip!"
        df_tooltip['tooltip'] = df_tooltip.apply(
            tooltip_gen,
            headers= options.get("headers"),
            axis=1
        )
        
        # Merge dataframe and pivoted dataframe
        df_tooltip = df_tooltip[[chart_options.get('id_field', 'cd_mun_ibge'), 'tooltip']]
        
        # Adding tooltips to detailed dataframe
        dataframe = pd.merge(
            dataframe,
            df_tooltip,
            left_on = chart_options.get('id_field', 'cd_mun_ibge'),
            right_on = chart_options.get('id_field', 'cd_mun_ibge'),
            how = "left"
        )
        dataframe['idx'] = dataframe[chart_options.get('id_field', 'cd_mun_ibge')]
        dataframe = dataframe.set_index('idx')
        
        grouped = dataframe.groupby(chart_options.get('layer_id','cd_indicador'))
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
                    name = group_names.get(group_id),
                    show = show
                )
                show = False

                # Generating circles
                for row_index, row in group.iterrows():
                    CircleMarker(
                        location=[row[chart_options.get('lat','latitude')], row[chart_options.get('long','longitude')]],
                        radius=row['radius'],
                        popup=row['tooltip'],
                        color=color,
                        fill=True,
                        fill_color=color
                    ).add_to(layer)
                
                # Adding layer to map
                layer.add_to(n)
            else:
                features = []
                for row_index, row in group.iterrows():
                    features.append({
                        'type': 'Feature',
                        'geometry': {
                            'type':'Point', 
                            'coordinates':[row[chart_options.get('long','longitude')], row[chart_options.get('lat','latitude')]]
                        },
                        'properties': {
                            'time': pd.to_datetime(row[chart_options.get('timeseries', 'nu_competencia')], format='%Y').__str__(),
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
                    # name = group_names.get(group_id),
                    # show = show,
                    period = 'P1Y',
                    duration = 'P1Y',
                    date_options='YYYY',
                    transition_time = 1000,
                    auto_play = True).add_to(n)
                    
                show = False

        n = self.add_au_marker(n, dataframe, au, options, chart_options)    
        
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
