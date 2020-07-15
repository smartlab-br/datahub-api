''' Class for instantiating chart objects '''
from model.charts.maps.choropleth import Choropleth
from model.charts.maps.heat import Heat
from model.charts.maps.cluster import Cluster
from model.charts.maps.bubbles import Bubbles
from model.charts.bar import BarHorizontal, BarVertical, \
    BarHorizontalStacked, BarVerticalStacked, \
    BarHorizontalPyramid, BarVerticalPyramid
from model.charts.line import Line, LineArea

class ChartFactory():
    ''' Factory to instantiate the correct chart implementation '''
    @classmethod
    def create(cls, options):
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
            # options.get('chart_options')["colorArray"] = ["#FF0000", "blue", "green"]

            # TODO - [REMOVE] Options for horizontal bars
            # options['chart_options']['orientation'] = "horizontal"                         
            # options['chart_options']['y'] = "nu_competencia"
            # options['chart_options']['x'] = "vl_indicador"
            # options['chart_options']['show_x_axis'] = False
            # options['chart_options']['show_y_axis'] = True

            # TODO - [REMOVE] Options for stacked bars
            # options.get('chart_options')['stacked'] = True
        
            # TODO - [REMOVE] Options for horizontal pyramid bars
            # options.get('chart_options')['left'] = ['Feminino']
            # options['chart_options']['orientation'] = "horizontal"                         
            # options['chart_options']['y'] = "cut"
            # options['chart_options']['x'] = "agr_count"
            # options['chart_options']['show_x_axis'] = False
            # options['chart_options']['show_y_axis'] = True
            # del options['chart_options']['legend_field']
            return cls.select_bar_by_options(options)
        if options.get('chart_type') == 'LINE':
            # TODO - [REMOVE] Options for stacked lines
            # options.get('chart_options')['stacked'] = True
            return cls.select_bar_by_options(options)

    @staticmethod
    def select_bar_by_options(options):
        orientation = options.get('chart_options', {}).get('orientation', 'horizontal')
        is_stacked = options.get('chart_options', {}).get('stacked', False)
        is_pyramid = options.get('chart_options', {}).get('left', False)
        if is_pyramid:
            if orientation == 'vertical':
                return BarVerticalPyramid(options.get('style_theme', 'light_minimal'))
            return BarHorizontalPyramid(options.get('style_theme', 'light_minimal'))
        if is_stacked:
            if orientation == 'vertical':
                return BarVerticalStacked(options.get('style_theme', 'light_minimal'))
            return BarHorizontalStacked(options.get('style_theme', 'light_minimal'))
        if orientation == 'vertical':
            return BarVertical(options.get('style_theme', 'light_minimal'))
        return BarHorizontal(options.get('style_theme', 'light_minimal'))

    @staticmethod
    def select_line_by_options(options):
        is_stacked = options.get('chart_options', {}).get('stacked', False)
        if is_stacked:
            return LineArea(options.get('style_theme', 'light_minimal'))
        return Line(options.get('style_theme', 'light_minimal'))