''' Class for drawing bar charts '''
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from service.viewconf_reader import ViewConfReader
from model.charts.base import BaseCartesianChart
from bokeh.io import curdoc

class Line(BaseCartesianChart):
    ''' Class for drawing bar charts '''
    LINE_WIDTH = 4

    def __init__(self, style_theme):
        curdoc().theme = style_theme

    def draw(self, dataframe, options):
        ''' Draws the line chart '''
        series = sorted(dataframe[options.get('chart_options', {}).get('id')].unique())
        if list(series):
            legend_names = self.get_legend_names(dataframe, options)

            # Chart initial setup
            chart = figure(tooltips=self.build_tooltip(options))
            chart.y_range.start = dataframe[options.get('chart_options').get('y')].min()
            chart = self.chart_config(chart, options)

            grouped = dataframe.groupby(options.get('chart_options').get('id'))
            serie_index = 0
            for group_id, group in grouped:
                chart.line(
                    options.get('chart_options').get('x'),
                    options.get('chart_options').get('y'),
                    source=ColumnDataSource(data=group.to_dict(orient='list')),
                    line_width=self.LINE_WIDTH,
                    line_color=self.get_fill_color(serie_index, options),
                    legend_label=legend_names.get(group_id)
                )
                serie_index = serie_index + 1
            # chart.add_tools(HoverTool(tooltips=[(hdr.get('text'), f"@{hdr.get('value')}") for hdr in options.get('headers')]))
        else:
            chart = figure(tooltips=self.build_tooltip(options))
            chart.y_range.start = dataframe[options.get('chart_options').get('y')].min()
            chart.line(
                options.get('chart_options').get('x'),
                options.get('chart_options').get('y'),
                source=ColumnDataSource(data=dataframe.to_dict(orient='list')),
                line_width=self.LINE_WIDTH
            )

        return chart

    @staticmethod
    def chart_config(chart, options):
        ''' Adds common chart configurations, according to given options '''
        # General config
        chart.axis.major_label_text_font = 'Palanquin'
        chart.axis.major_tick_line_color = None
        chart.axis.minor_tick_line_color = None
        chart.x_range.range_padding = 0.0

        # Removing grid lines
        chart.xgrid.grid_line_color = None
        chart.ygrid.grid_line_color = None

        # Axis visibility
        if not options.get('chart_options', {}).get('show_x_axis', True):
            chart.xaxis.visible = False
        if not options.get('chart_options', {}).get('show_y_axis', True):
            chart.yaxis.visible = False

        # Legend config
        chart.legend.label_text_font = 'Palanquin'
        chart.legend.location = "top_right"
        chart.legend.orientation = "vertical"

        # Ticks formatting
        chart.yaxis.formatter = NumeralTickFormatter(format="0.00a")

        return chart

    @staticmethod
    def get_fill_color(index, options):
        ''' Gets the positional color in the scale built according to given options '''
        return ViewConfReader.get_color_scale(options)[index]

    @staticmethod
    def get_legend_names(dataframe, options):
        ''' Get series' names that should be plotted in legend '''
        if options.get('chart_options', {}).get('legend_field') in dataframe.columns:
            tmp = dataframe[[options.get('chart_options').get('id'), options.get('chart_options').get('legend_field')]].drop_duplicates().set_index(options.get('chart_options').get('id')).to_dict()
            return tmp.get(options.get('chart_options').get('legend_field'))
        return {i: i for i in dataframe[options.get('chart_options').get('id')].unique()}

    @staticmethod
    def build_tooltip(options):
        ''' Builds the tooltip HTML based on given options '''
        rows = [f'<tr style="text-align: left;"><th style="padding: 4px; padding-right: 10px;">{hdr.get("text")}</th><td style="padding: 4px;">@{hdr.get("value")}</td></tr>' for hdr in options.get('headers')]
        return f"<table>{''.join(rows)}</table>"

class LineArea(Line):
    ''' Class for drawing bar charts '''
    def draw(self, dataframe, options):
        series = sorted(dataframe[options.get('chart_options', {}).get('id')].unique())
        if list(series):
            data = self.pivot_dataframe(dataframe, options)

            # Chart initial setup
            chart = figure()
            chart.y_range.start = dataframe[options.get('chart_options').get('y')].min()
            chart = self.chart_config(chart, options)

            chart.varea_stack(
                series,
                x=options.get('chart_options').get('x'),
                color=ViewConfReader.get_color_scale(options),
                source=data
            )
        else:
            chart = figure(tooltips=self.build_tooltip(options))
            chart.y_range.start = dataframe[options.get('chart_options').get('y')].min()
            chart.line(
                options.get('chart_options').get('x'),
                options.get('chart_options').get('y'),
                source=ColumnDataSource(data=dataframe.to_dict(orient='list')),
                line_width=self.LINE_WIDTH
            )

        return chart
