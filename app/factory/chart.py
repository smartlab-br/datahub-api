''' Class for instantiating chart objects '''
from model.charts.maps.choropleth import Choropleth
from model.charts.maps.heat import Heat
from model.charts.maps.cluster import Cluster
from model.charts.maps.bubbles import Bubbles
from model.charts.bar import BarHorizontal, BarVertical #, BarHorizontalStacked, BarVerticalStacked

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
            orientation = options.get('chart_options', {}).get('orientation', 'horizontal')
            is_stacked = options.get('chart_options', {}).get('stacked', False)
            if is_stacked:
                if orientation == 'vertical':
                    # return BarVerticalStacked()
                    pass
                # return BarHorizontalStacked()
                pass
            elif orientation == 'vertical':
                return BarVertical()
            return BarHorizontal()
        pass
    
        
