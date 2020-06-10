''' Model for fetching chart '''
import folium
import numpy as np
from folium.plugins import HeatMap
from service.viewconf_reader import ViewConfReader

##### With time series #####
# from folium import plugins

# map_hooray = folium.Map(location=[51.5074, 0.1278],
#                     zoom_start = 13) 

# # Ensure you're handing it floats
# df_acc['Latitude'] = df_acc['Latitude'].astype(float)
# df_acc['Longitude'] = df_acc['Longitude'].astype(float)

# # Filter the DF for rows, then columns, then remove NaNs
# heat_df = df_acc[df_acc['Speed_limit']=='40'] # Reducing data size so it runs faster
# heat_df = df_acc[df_acc['Year']=='2007'] # Reducing data size so it runs faster
# heat_df = heat_df[['Latitude', 'Longitude']]

# # Create weight column, using date
# heat_df['Weight'] = df_acc['Date'].str[3:5]
# heat_df['Weight'] = heat_df['Weight'].astype(float)
# heat_df = heat_df.dropna(axis=0, subset=['Latitude','Longitude', 'Weight'])

# # List comprehension to make out list of lists
# heat_data = [[[row['Latitude'],row['Longitude']] for index, row in heat_df[heat_df['Weight'] == i].iterrows()] for i in range(0,13)]

# # Plot it on the map
# hm = plugins.HeatMapWithTime(heat_data,auto_play=True,max_opacity=0.8)
# hm.add_to(map_hooray)
# # Display the map
# map_hooray
##### #####

class Heat():
    ''' Heatmap building class '''
    @staticmethod
    def draw(dataframe, options):
        ''' Gera um mapa topojson a partir das opções enviadas '''
        # http://localhost:5000/charts/choropleth?from_viewconf=S&au=2927408&card_id=mapa_pib_brasil&dimension=socialeconomico&as_image=S
        # Default values
        # tiles_url = 'http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png'
        tiles_url = 'https://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}'
        # tiles_attribution = '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        tiles_attribution = 'Esri, USGS | Esri, HERE | Esri, Garmin, FAO, NOAA'
        visao = options.get('visao', 'uf')

        style_statement = "<link href='https://fonts.googleapis.com/css2?family=Pathway+Gothic+One&display=swap' rel='stylesheet'>\
            <style>\
                .legend.leaflet-control{display:none}\
                .leaflet-tooltip table tbody tr:first-child th{display:none;}\
                .leaflet-tooltip table tbody tr:first-child td{\
                    font-family: 'Pathway Gothic One', Calibri, sans-serif;\
                    font-size: 2.5em;\
                    font-weight: 700;\
                }\
                .leaflet-tooltip table tbody tr:nth-child(2){\
                    border-top: 1px solid black;\
                }\
                path.leaflet-interactive:hover {\
                    fill-opacity: 1;\
                }\
            </style>"

        au = options.get('au')
        chart_options = options.get('chart_options')

        dataframe['str_id'] = dataframe[chart_options.get('id_field', 'cd_mun_ibge')].astype(str)
        dataframe['idx'] = dataframe[chart_options.get('id_field', 'cd_mun_ibge')]
        
        # Runs dataframe modifiers from viewconf
        dataframe = ViewConfReader().generate_columns(dataframe, options)

        dataframe = dataframe.set_index('idx')
        centroide = None  
        marker_tooltip = ''
        # for each_au in state_geo.get('features'):
        # for each_au in state_geo.get('objects',{}).get('data',{}).get('geometries',[]):
        #     # During topo conversion, all ID will be named smartlab_geo_id and
        #     # all NAME will be in an attribute called smartlab_geo_name.
        #     try:
        #         df_row = dataframe.loc[int(each_au.get('properties').get("smartlab_geo_id"))]
        #         each_au.get('properties').update(json.loads(df_row.to_json()), headers=options.get('headers'))
        #     except KeyError:
        #         df_row = {hdr.get('value'): 'N/A' for hdr in options.get('headers')}
        #         df_row[options.get('headers')[0].get('value')] = each_au.get('properties').get('smartlab_geo_name')
        #         each_au.get('properties').update(json.loads(json.dumps(df_row)), headers=options.get('headers'))
        #     if str(each_au.get('properties', {}).get(chart_options.get('id_field'))) == str(au):
        #         centroide = each_au.get('properties', {}).get('centroide')
        #         if centroide:
        #             centroide.reverse()
                
        #         marker_tooltip = "".join([f"<tr style='text-align: left;'><th style='padding: 4px; padding-right: 10px;'>{hdr.get('text').encode('ascii', 'xmlcharrefreplace').decode()}</th><td style='padding: 4px;'>{str(df_row[hdr.get('value')]).encode('ascii', 'xmlcharrefreplace').decode()}</td></tr>" for hdr in options.get('headers')])
        #         marker_tooltip = f"<table>{marker_tooltip}</table>"
        
        # Creating map instance
        n = folium.Map(tiles=tiles_url, attr = tiles_attribution, control_scale = True)

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
        group_names = { hdr.get('layer_id'): hdr.get('text') for hdr in options.get('headers') }

        grouped = dataframe.groupby(chart_options.get('layer_id','cd_indicador'))
        show = True # Shows only the first
        for group_id, group in grouped:
            chart = HeatMap(
                group[cols].values.tolist(),
                name = group_names.get(group_id),
                show = show
            )
            show = False
            chart.add_to(n)
            
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
            print(au_title)

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

        n.get_root().header.add_child(folium.Element(style_statement))

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
