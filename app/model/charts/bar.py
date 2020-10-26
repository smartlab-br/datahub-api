''' Class for drawing barcharts '''
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.transform import dodge
import pandas as pd
from bokeh.io import curdoc
from model.charts.base import BaseCartesianChart
from service.viewconf_reader import ViewConfReader

class Bar(BaseCartesianChart):
    ''' Class for drawing bar charts '''
    BAR_SIZE = 0.8

    # TODO Style 1 - Add text to bar
    #     chart_options:
    #       text: "vl_indicador"

    # TODO Final - Responsivity
    def __init__(self, options, dataframe):
        super().__init__(options, dataframe)
        curdoc().theme = options.get('style_theme', 'light_minimal')

    def draw(self):
        ''' Abstract method - must be implemented '''
        raise NotImplementedError

    def chart_config(self, chart):
        chart = super().chart_config(chart, self.options)

        # Axis visibility
        if self.options is None or not self.options.get('chart_options', {}).get('show_x_axis', False):
            chart.xaxis.visible = False
        if self.options is None or not self.options.get('chart_options', {}).get('show_y_axis', False):
            chart.yaxis.visible = False

        return chart

class BarVertical(Bar):
    ''' Class for drawing bar charts '''
    def draw(self):
        # Chart initial setup
        self.dataframe[self.options.get('chart_options').get('x')] = self.dataframe[self.options.get('chart_options').get('x')].astype(str)
        chart = figure(
            tooltips=self.build_tooltip(self.options),
            x_range=list(self.dataframe[self.options.get('chart_options').get('x')].sort_values().unique().astype(str))
        )
        chart.y_range.start = 0
        chart = self.chart_config(chart, self.options)

        series = sorted(self.dataframe[self.options.get('chart_options', {}).get('id')].unique())
        if list(series):
            legend_names = self.get_legend_names(self.dataframe, self.options)

            # Create bars
            bar_width = self.BAR_SIZE / len(series)
            pos = -self.BAR_SIZE / 2

            grouped = self.dataframe.groupby(self.options.get('chart_options').get('id'))
            serie_index = 0
            for group_id, group in grouped:
                chart.vbar(
                    x=dodge(
                        self.options.get('chart_options').get('x'),
                        pos,
                        range=chart.x_range
                    ),
                    top=self.options.get('chart_options').get('y'),
                    width=bar_width - 0.05,
                    source=ColumnDataSource(data=group.to_dict(orient='list')),
                    color=self.get_fill_color(serie_index, self.options),
                    legend_label=legend_names.get(group_id)
                )
                pos = pos + bar_width
                serie_index = serie_index + 1
        else:
            chart.vbar(
                x=self.options.get('chart_options', {}).get('x'),
                top=self.options.get('chart_options', {}).get('y'),
                source=ColumnDataSource(data=self.dataframe.to_dict(orient='list')),
                width=self.BAR_SIZE
            )
        return chart

class BarHorizontal(Bar):
    ''' Class for drawing bar charts '''
    def draw(self):
        # Chart initial setup
        self.dataframe[self.options.get('chart_options').get('x')] = self.dataframe[self.options.get('chart_options').get('x')].astype(str)
        chart = figure(
            tooltips=self.build_tooltip(self.options),
            x_range=list(self.dataframe[self.options.get('chart_options').get('x')].sort_values().unique().astype(str))
        )
        chart.x_range.start = 0
        chart = self.chart_config(chart, self.options)

        series = sorted(self.dataframe[self.options.get('chart_options', {}).get('id')].unique())
        if list(series):
            legend_names = self.get_legend_names(self.dataframe, self.options)

            # Create bars
            bar_width = self.BAR_SIZE / len(series)
            pos = -self.BAR_SIZE / 2

            grouped = self.dataframe.groupby(self.options.get('chart_options').get('id'))
            serie_index = 0
            for group_id, group in grouped:
                chart.hbar(
                    y=dodge(
                        self.options.get('chart_options').get('y'),
                        pos,
                        range=chart.y_range
                    ),
                    right=self.options.get('chart_options').get('x'),
                    height=bar_width - 0.05,
                    source=ColumnDataSource(data=group.to_dict(orient='list')),
                    color=self.get_fill_color(serie_index, self.options),
                    legend_label=legend_names.get(group_id)
                )

                pos = pos + bar_width
                serie_index = serie_index + 1
        else:
            chart.hbar(
                y=list(self.dataframe[self.options.get('chart_options', {}).get('y')]),
                right=list(self.dataframe[self.options.get('chart_options', {}).get('x')]),
                source=ColumnDataSource(data=self.dataframe.to_dict(orient='list')),
                width=self.BAR_SIZE
            )

        return chart

class BarVerticalStacked(Bar):
    ''' Class for drawing bar charts '''
    def draw(self):
        series = sorted(self.dataframe[self.options.get('chart_options', {}).get('id')].unique())
        if list(series):
            legend_names = self.get_legend_names(self.dataframe, self.options)
            data = self.pivot_dataframe(self.dataframe, self.options)

            # Chart initial setup
            chart = figure(x_range=data.get(self.options.get('chart_options').get('x')))
            chart.y_range.start = 0
            chart = self.chart_config(chart, self.options)
            chart = self.generate_stacks(
                chart, data=data, series=series,
                legend_names=legend_names, options=self.options
            )
        else:
            chart = figure(x_range=sorted(list(self.dataframe[self.options.get('chart_options', {}).get('x')])))
            chart.y_range.start = 0
            chart.vbar(
                x=list(self.dataframe[self.options.get('chart_options', {}).get('x')]),
                top=list(self.dataframe[self.options.get('chart_options', {}).get('y')]),
                width=self.BAR_SIZE
            )
        return chart

    def generate_stacks(self, chart, **kwargs):
        ''' Create bars '''
        chart.vbar_stack(
            kwargs.get('series'),
            x=kwargs.get('options', {}).get('chart_options', {}).get('x'),
            width=self.BAR_SIZE,
            color=ViewConfReader.get_color_scale(kwargs.get('options')),
            source=kwargs.get('data'),
            legend_label=[v for _k, v in kwargs.get('legend_names').items()]
        )
        return chart

class BarHorizontalStacked(Bar):
    ''' Class for drawing bar charts '''
    def draw(self):
        series = sorted(self.dataframe[self.options.get('chart_options', {}).get('id')].unique())
        if list(series):
            # Get legend names dictionary
            legend_names = self.get_legend_names(self.dataframe, self.options)
            # Pivot dataframe
            src = self.dataframe.copy()
            src = pd.pivot_table(
                src,
                values=[self.options.get('chart_options').get('x')],
                columns=self.options.get('chart_options').get('id'),
                index=self.options.get('chart_options').get('y'),
                aggfunc="sum",
                fill_value=0
            )
            src.columns = src.columns.droplevel()
            src = src.reset_index()
            src[self.options.get('chart_options').get('y')] = src[self.options.get('chart_options').get('y')].astype(str)
            data = {col:list(src[col]) for col in src.columns}

            # Chart initial setup
            chart = figure(y_range=data.get(self.options.get('chart_options').get('y')))
            chart.x_range.start = 0
            chart = self.chart_config(chart, self.options)
            chart = self.generate_stacks(
                chart, data=data, series=series,
                legend_names=legend_names, options=self.options
            )
        else:
            chart = figure(y_range=sorted(list(self.dataframe[self.options.get('chart_options', {}).get('x')])))
            chart.x_range.start = 0
            chart.hbar(
                y=list(self.dataframe[self.options.get('chart_options', {}).get('y')]),
                right=list(self.dataframe[self.options.get('chart_options', {}).get('x')]),
                width=self.BAR_SIZE
            )

        return chart

    def generate_stacks(self, chart, **kwargs):
        ''' Creates bars '''
        chart.hbar_stack(
            kwargs.get('series'),
            y=kwargs.get('options', {}).get('chart_options', {}).get('y'),
            height=self.BAR_SIZE,
            color=ViewConfReader.get_color_scale(kwargs.get('options')),
            source=kwargs.get('data'),
            legend_label=[v for _k, v in kwargs.get('legend_names').items()]
        )
        return chart

class BarPyramid():
    ''' Abstraction for pyramid charts '''
    @staticmethod
    def get_series(**kwargs):
        ''' Get series data and params to generate stack configs '''
        # series, data, options, legend_names, branch_direction, branch_value
        chart_options = kwargs.get('options', {}).get('chart_options')
        branch_series = [v for v in kwargs.get('series') if v in chart_options.get(kwargs.get('branch_direction'))]

        if kwargs.get('branch_direction', 'right') == 'left':
            branch_data = {k:[-v_item for v_item in v] for k, v in kwargs.get('data').items() if k in branch_series}
            branch_color = ViewConfReader.get_color_scale(kwargs.get('options'))[-len(branch_series)]
        else:
            branch_data = {k:v for k, v in kwargs.get('data').items() if k in branch_series}
            branch_color = ViewConfReader.get_color_scale(kwargs.get('options'))[:len(branch_series)]

        branch_data[chart_options.get(kwargs.get('branch_value'))] = kwargs.get('data').get(chart_options.get(kwargs.get('branch_value')))
        branch_legend_labels = [v for _k, v in kwargs.get('legend_names').items() if _k in chart_options.get(kwargs.get('branch_direction'))]

        return (branch_series, branch_data, branch_legend_labels, branch_color)

    def generate_pyramid_stacks(self, chart, **kwargs):
        ''' Generates pyramid's bar stacks '''
        min_val = 0
        options = kwargs.get('options')
        options['chart_options']['right'] = [
            s
            for
            s
            in
            kwargs.get('series')
            if s not in options.get('chart_options', {}).get('left')
        ]
        for serie in kwargs.get('series'):
            # Identify the series direction (check if value is on 'left' chart option attribute)
            direction = 'right' # Positive branch
            if serie in options.get('chart_options').get('left'): # Negative Branch
                direction = 'left'
            # Get branch configurations from data and series
            (b_series, b_data, b_legend_labels, b_color) = self.get_series(
                series=kwargs.get('series'), data=kwargs.get('data'),
                options=options, legend_names=kwargs.get('legend_names'),
                branch_direction=direction,
                branch_value='y'
            )
            # Updates the minimum value
            if direction == 'left':
                min_val = min_val + min(b_data.get(serie, {}))
            chart = self.create_bar(
                chart, series=b_series, data=b_data,
                legend_labels=b_legend_labels, color=b_color
            )

        return (chart, min_val)

    def create_bar(self, chart, **kwargs):
        ''' Abstract method - must be implemented '''
        raise NotImplementedError

class BarVerticalPyramid(BarPyramid, BarVerticalStacked):
    ''' Class for drawing bar charts '''
    def generate_stacks(self, chart, **kwargs):
        ''' Redirects the generate method to pyramid abstraction '''
        (chart, min_val) = self.generate_pyramid_stacks(chart, **kwargs)
        chart.y_range.start = min_val
        return chart

    def create_bar(self, chart, **kwargs):
        ''' Creates the bar '''
        chart.vbar_stack(
            kwargs.get('series'),
            x=self.options.get('chart_options').get('x'),
            height=self.BAR_SIZE,
            color=kwargs.get('color'),
            source=kwargs.get('data'),
            legend_label=kwargs.get('legend_labels')
        )
        return chart

class BarHorizontalPyramid(BarHorizontalStacked, BarPyramid):
    ''' Class for drawing bar charts '''
    def generate_stacks(self, chart, **kwargs):
        ''' Redirects the generate method to pyramid abstraction '''
        (chart, min_val) = self.generate_pyramid_stacks(chart, **kwargs)
        chart.x_range.start = min_val
        return chart

    def create_bar(self, chart, **kwargs):
        ''' Creates the bar '''
        chart.hbar_stack(
            kwargs.get('series'),
            y=self.options.get('chart_options').get('y'),
            height=self.BAR_SIZE,
            color=kwargs.get('color'),
            source=kwargs.get('data'),
            legend_label=kwargs.get('legend_labels')
        )
        return chart
