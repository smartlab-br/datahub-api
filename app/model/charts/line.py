''' Class for drawing bar charts '''
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.io import curdoc
from service.viewconf_reader import ViewConfReader
from model.charts.base import BaseCartesianChart

class Line(BaseCartesianChart):
    ''' Class for drawing bar charts '''
    LINE_WIDTH = 4

    def __init__(self, style_theme='light_minimal'):
        curdoc().theme = style_theme

    def draw(self):
        ''' Draws the line chart '''
        series = sorted(self.dataframe[self.options.get('chart_options', {}).get('id')].unique())
        if list(series):
            legend_names = self.get_legend_names(self.dataframe, self.options)

            # Chart initial setup
            chart = figure(tooltips=self.build_tooltip(self.options))
            chart.y_range.start = self.dataframe[self.options.get('chart_options').get('y')].min()
            chart = self.chart_config(chart, self.options)

            grouped = self.dataframe.groupby(self.options.get('chart_options').get('id'))
            serie_index = 0
            for group_id, group in grouped:
                chart.line(
                    self.options.get('chart_options').get('x'),
                    self.options.get('chart_options').get('y'),
                    source=ColumnDataSource(data=group.to_dict(orient='list')),
                    line_width=self.LINE_WIDTH,
                    line_color=self.get_fill_color(serie_index, self.options),
                    legend_label=legend_names.get(group_id)
                )
                serie_index = serie_index + 1
            # chart.add_tools(HoverTool(tooltips=[(hdr.get('text'), f"@{hdr.get('value')}") for hdr in options.get('headers')]))
        else:
            chart = figure(tooltips=self.build_tooltip(self.options))
            chart.y_range.start = self.dataframe[self.options.get('chart_options').get('y')].min()
            chart.line(
                self.options.get('chart_options').get('x'),
                self.options.get('chart_options').get('y'),
                source=ColumnDataSource(data=self.dataframe.to_dict(orient='list')),
                line_width=self.LINE_WIDTH
            )

        return chart

    def chart_config(self, chart):
        ''' Adds common chart configurations, according to given options '''
        chart = super().chart_config(chart)
        chart.x_range.range_padding = 0.0

        # Axis visibility
        if self.options is None:
            chart.xaxis.visible = True
            chart.yaxis.visible = True
        else:
            if not self.options.get('chart_options', {}).get('show_x_axis', True):
                chart.xaxis.visible = False
            if not self.options.get('chart_options', {}).get('show_y_axis', True):
                chart.yaxis.visible = False

        # Ticks formatting
        chart.yaxis.formatter = NumeralTickFormatter(format="0.00a")

        return chart

class LineArea(Line):
    ''' Class for drawing bar charts '''
    def draw(self):
        series = sorted(self.dataframe[self.options.get('chart_options', {}).get('id')].unique())
        if list(series):
            data = self.pivot_dataframe(self.dataframe, self.options)

            # Chart initial setup
            chart = figure()
            chart.y_range.start = self.dataframe[self.options.get('chart_options').get('y')].min()
            chart = self.chart_config(chart)

            chart.varea_stack(
                series,
                x=self.options.get('chart_options').get('x'),
                color=ViewConfReader.get_color_scale(self.options),
                source=data
            )
        else:
            chart = figure(tooltips=self.build_tooltip(self.options))
            chart.y_range.start = self.dataframe[self.options.get('chart_options').get('y')].min()
            chart.line(
                self.options.get('chart_options').get('x'),
                self.options.get('chart_options').get('y'),
                source=ColumnDataSource(data=self.dataframe.to_dict(orient='list')),
                line_width=self.LINE_WIDTH
            )

        return chart
