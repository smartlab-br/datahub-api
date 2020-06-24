''' Class for instantiating chart objects '''
from model.charts.maps.choropleth import Choropleth
from model.charts.maps.heat import Heat
from model.charts.maps.cluster import Cluster
from model.charts.maps.bubbles import Bubbles
from model.charts.bar import BarHorizontal, BarVertical, BarHorizontalStacked, BarVerticalStacked

class ChartFactory():
    ''' Factory to instantiate the correct chart implementation '''
    @staticmethod
    def create(options):
        ''' Factory method '''
        if options.get('chart_type') == 'MAP_TOPOJSON':
            return Choropleth()
        if options.get('chart_type') == 'MAP_HEAT':
            return Heat()
        if options.get('chart_type') == 'MAP_CLUSTER':
            return Cluster()
        if options.get('chart_type') == 'MAP_BUBBLES':
            return Bubbles()
        if options.get('chart_type') == 'BAR':
            # TODO - [REMOVE] Options for color testing
            options.get('chart_options')["colorArray"] = ["#FF0000", "blue", "green"]

            # TODO - [REMOVE] Options for horizontal bars
            options['chart_options']['orientation'] = "horizontal"                         
            options['chart_options']['y'] = "nu_competencia"
            options['chart_options']['x'] = "vl_indicador"
            options['chart_options']['show_x_axis'] = False
            options['chart_options']['show_y_axis'] = True

            # TODO - [REMOVE] Options for stacked bars
            options.get('chart_options')['stacked'] = True

            orientation = options.get('chart_options', {}).get('orientation', 'horizontal')
            is_stacked = options.get('chart_options', {}).get('stacked', False)
            if is_stacked:
                if orientation == 'vertical':
                    return BarVerticalStacked()
                return BarHorizontalStacked()
            elif orientation == 'vertical':
                return BarVertical()
            return BarHorizontal()
        pass
    
        
