""" Class for instantiating chart objects """
from model.charts.maps.choropleth import Choropleth
from model.charts.maps.heat import Heat
from model.charts.maps.cluster import Cluster
from model.charts.maps.bubbles import Bubbles
from model.charts.maps.mixed import Mixed
from model.charts.bar import BarHorizontal, BarVertical, \
    BarHorizontalStacked, BarVerticalStacked, \
    BarHorizontalPyramid, BarVerticalPyramid
from model.charts.line import Line, LineArea


class ChartFactory:
    """ Factory to instantiate the correct chart implementation """
    @classmethod
    def create(cls, options, dataframe=None, mixed_type=None):
        """ Factory method """
        chart = None
        if options is None:
            options = {"chart_type": "LINE"}
        if mixed_type:
            if mixed_type == 'MIXED_MAP':
                chart = Mixed([cls.create(each_option, each_dataframe) for each_option, each_dataframe in zip(options, dataframe)])
        else:
            if options.get('chart_type') == 'MAP_TOPOJSON':
                chart = Choropleth(options, dataframe)
            if options.get('chart_type') == 'MAP_HEAT':
                chart = Heat(options, dataframe)
            if options.get('chart_type') == 'MAP_CLUSTER':
                chart = Cluster(options, dataframe)
            if options.get('chart_type') == 'MAP_BUBBLES':
                chart = Bubbles(options, dataframe)
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
                chart = cls.select_bar_by_options(options, dataframe)
            if options.get('chart_type') == 'LINE':
                # TODO - [REMOVE] Options for stacked lines
                # options.get('chart_options')['stacked'] = True
                chart = cls.select_line_by_options(options, dataframe)
        return chart

    @staticmethod
    def select_bar_by_options(options, dataframe):
        """ Select the adequate BAR implementation, according to options """
        orientation = options.get('chart_options', {}).get('orientation', 'horizontal')
        is_stacked = options.get('chart_options', {}).get('stacked', False)
        is_pyramid = options.get('chart_options', {}).get('left', False)
        if is_pyramid:
            if orientation == 'vertical':
                return BarVerticalPyramid(options, dataframe)
            return BarHorizontalPyramid(options, dataframe)
        if is_stacked:
            if orientation == 'vertical':
                return BarVerticalStacked(options, dataframe)
            return BarHorizontalStacked(options, dataframe)
        if orientation == 'vertical':
            return BarVertical(options, dataframe)
        return BarHorizontal(options, dataframe)

    @staticmethod
    def select_line_by_options(options, dataframe):
        """ Select the adequate LINE implementation, according to options """
        is_stacked = options.get('chart_options', {}).get('stacked', False)
        if is_stacked:
            return LineArea(options, dataframe)
        return Line(options, dataframe)
