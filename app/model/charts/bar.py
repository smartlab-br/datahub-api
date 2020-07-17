''' Class for drawing barcharts '''
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.transform import dodge
import pandas as pd
from model.charts.base import BaseCartesianChart
from service.viewconf_reader import ViewConfReader
from bokeh.io import curdoc

class Bar(BaseCartesianChart):
    ''' Class for drawing bar charts '''
    BAR_SIZE = 0.8

    # TODO Style 1 - Add text to bar
    #     chart_options:
    #       text: "vl_indicador"

    # TODO Final - Responsivity
    def __init__(self, style_theme):
        curdoc().theme = style_theme

    def draw(self, dataframe, options):
        ''' Abstract method - must be implemented '''
        raise NotImplementedError

    def chart_config(self, chart, options):
        # General config
        chart.axis.major_label_text_font = 'Palanquin'
        chart.axis.major_tick_line_color = None
        chart.axis.minor_tick_line_color = None

        # Removing grid lines
        chart.xgrid.grid_line_color = None
        chart.ygrid.grid_line_color = None

        # Axis visibility
        if not options.get('chart_options', {}).get('show_x_axis', False):
            chart.xaxis.visible = False
        if not options.get('chart_options', {}).get('show_y_axis', False):
            chart.yaxis.visible = False

        # Legend config
        chart.legend.label_text_font = 'Palanquin'
        chart.legend.location = "top_right"
        chart.legend.orientation = "vertical"

        return chart

    def get_fill_color(self, index, options):
        return ViewConfReader.get_color_scale(options)[index]

    def get_legend_names(self, dataframe, options):
        if options.get('chart_options').get('legend_field') and options.get('chart_options').get('legend_field') in dataframe.columns:
            dataframe[options.get('chart_options').get('legend_field')] = dataframe[options.get('chart_options').get('id')]
            tmp = dataframe[[options.get('chart_options').get('id'), options.get('chart_options').get('legend_field')]].drop_duplicates().set_index(options.get('chart_options').get('id')).to_dict()
            return tmp.get(options.get('chart_options').get('legend_field'))
        return {i: i for i in dataframe[options.get('chart_options').get('id')].unique()}

    def build_tooltip(self, options):
        rows = [f'<tr style="text-align: left;"><th style="padding: 4px; padding-right: 10px;">{hdr.get("text")}</th><td style="padding: 4px;">@{hdr.get("value")}</td></tr>' for hdr in options.get('headers')]
        return f"<table>{''.join(rows)}</table>"

class BarVertical(Bar):
    ''' Class for drawing bar charts '''
    def draw(self, dataframe, options):
        # Chart initial setup
        dataframe[options.get('chart_options').get('x')] = dataframe[options.get('chart_options').get('x')].astype(str)
        chart = figure(
            tooltips=self.build_tooltip(options),
            x_range=list(dataframe[options.get('chart_options').get('x')].sort_values().unique().astype(str))
        )
        chart.y_range.start = 0
        chart = self.chart_config(chart, options)

        series = sorted(dataframe[options.get('chart_options', {}).get('id')].unique())
        if list(series):
            legend_names = self.get_legend_names(dataframe, options)

            # Create bars
            bar_width = self.BAR_SIZE / len(series)
            pos = -self.BAR_SIZE / 2

            grouped = dataframe.groupby(options.get('chart_options').get('id'))
            serie_index = 0
            for group_id, group in grouped:
                chart.vbar(
                    x=dodge(
                        options.get('chart_options').get('x'),
                        pos,
                        range=chart.x_range
                    ),
                    top=options.get('chart_options').get('y'),
                    width=bar_width - 0.05,
                    source=ColumnDataSource(data=group.to_dict(orient='list')),
                    color=self.get_fill_color(serie_index, options),
                    legend_label=legend_names.get(group_id)
                )
                pos = pos + bar_width
                serie_index = serie_index + 1
        else:
            chart.vbar(
                x=options.get('chart_options', {}).get('x'),
                top=options.get('chart_options', {}).get('y'),
                source=ColumnDataSource(data=dataframe.to_dict(orient='list')),
                width=self.BAR_SIZE
            )
        return chart

class BarHorizontal(Bar):
    ''' Class for drawing bar charts '''
    def draw(self, dataframe, options):
        # Chart initial setup
        dataframe[options.get('chart_options').get('x')] = dataframe[options.get('chart_options').get('x')].astype(str)
        chart = figure(
            tooltips=self.build_tooltip(options),
            x_range=list(dataframe[options.get('chart_options').get('x')].sort_values().unique().astype(str))
        )
        chart.x_range.start = 0
        chart = self.chart_config(chart, options)

        series = sorted(dataframe[options.get('chart_options', {}).get('id')].unique())
        if list(series):
            legend_names = self.get_legend_names(dataframe, options)

            # Create bars
            bar_width = self.BAR_SIZE / len(series)
            pos = -self.BAR_SIZE / 2

            grouped = dataframe.groupby(options.get('chart_options').get('id'))
            serie_index = 0
            for group_id, group in grouped:
                chart.hbar(
                    y=dodge(
                        options.get('chart_options').get('y'),
                        pos,
                        range=chart.y_range
                    ),
                    right=options.get('chart_options').get('x'),
                    height=bar_width - 0.05,
                    source=ColumnDataSource(data=group.to_dict(orient='list')),
                    color=self.get_fill_color(serie_index, options),
                    legend_label=legend_names.get(group_id)
                )

                pos = pos + bar_width
                serie_index = serie_index + 1
        else:
            chart.hbar(
                y=list(dataframe[options.get('chart_options', {}).get('y')]),
                right=list(dataframe[options.get('chart_options', {}).get('x')]),
                source=ColumnDataSource(data=dataframe.to_dict(orient='list')),
                width=self.BAR_SIZE
            )

        return chart

class BarVerticalStacked(Bar):
    ''' Class for drawing bar charts '''
    def draw(self, dataframe, options):
        series = sorted(dataframe[options.get('chart_options', {}).get('id')].unique())
        if list(series):
            legend_names = self.get_legend_names(dataframe, options)
            data = self.pivot_dataframe(dataframe, options)

            # Chart initial setup
            chart = figure(x_range=data.get(options.get('chart_options').get('x')))
            chart.y_range.start = 0
            chart = self.chart_config(chart, options)
            chart = self.generate_stacks(chart, data, series, legend_names, options)
        else:
            chart = figure(x_range=sorted(list(dataframe[options.get('chart_options', {}).get('x')])))
            chart.y_range.start = 0
            chart.vbar(
                x=list(dataframe[options.get('chart_options', {}).get('x')]),
                top=list(dataframe[options.get('chart_options', {}).get('y')]),
                width=self.BAR_SIZE
            )
        return chart

    def generate_stacks(self, chart, data, series, legend_names, options):
        # Create bars
        chart.vbar_stack(
            series,
            x=options.get('chart_options').get('x'),
            width=self.BAR_SIZE,
            color=ViewConfReader.get_color_scale(options),
            source=data,
            legend_label=[v for _k, v in legend_names.items()]
        )
        return chart

class BarHorizontalStacked(Bar):
    ''' Class for drawing bar charts '''
    def draw(self, dataframe, options):
        series = sorted(dataframe[options.get('chart_options', {}).get('id')].unique())
        if list(series):
            # Get legend names dictionary
            legend_names = self.get_legend_names(dataframe, options)
            # Pivot dataframe
            src = dataframe.copy()
            src = pd.pivot_table(
                src,
                values=[options.get('chart_options').get('x')],
                columns=options.get('chart_options').get('id'),
                index=options.get('chart_options').get('y'),
                aggfunc="sum",
                fill_value=0
            )
            src.columns = src.columns.droplevel()
            src = src.reset_index()
            src[options.get('chart_options').get('y')] = src[options.get('chart_options').get('y')].astype(str)
            data = {col:list(src[col]) for col in src.columns}

            # Chart initial setup
            chart = figure(y_range=data.get(options.get('chart_options').get('y')))
            chart.x_range.start = 0
            chart = self.chart_config(chart, options)
            chart = self.generate_stacks(chart, data, series, legend_names, options)
        else:
            chart = figure(y_range=sorted(list(dataframe[options.get('chart_options', {}).get('x')])))
            chart.x_range.start = 0
            chart.hbar(
                y=list(dataframe[options.get('chart_options', {}).get('y')]),
                right=list(dataframe[options.get('chart_options', {}).get('x')]),
                width=self.BAR_SIZE
            )

        return chart

    def generate_stacks(self, chart, data, series, legend_names, options):
        # Create bars
        chart.hbar_stack(
            series,
            y=options.get('chart_options').get('y'),
            height=self.BAR_SIZE,
            color=ViewConfReader.get_color_scale(options),
            source=data,
            legend_label=[v for _k, v in legend_names.items()]
        )
        return chart

class BarVerticalPyramid(BarVerticalStacked):
    ''' Class for drawing bar charts '''
    def generate_stacks(self, chart, data, series, legend_names, options):
        # Create bars
        d_series = [v for v in series if v in options.get('chart_options').get('left')]
        u_series = [v for v in series if v not in options.get('chart_options').get('left')]

        d_data = {k:[-v_item for v_item in v] for k, v in data.items() if k in d_series}
        u_data = {k:v for k, v in data.items() if k in u_series}

        # Getting minimum value
        chart.y_range.start = min([min(v) for _k, v in d_data.items()])

        # Adding categories column
        d_data[options.get('chart_options').get('y')] = data.get(options.get('chart_options').get('y'))
        u_data[options.get('chart_options').get('y')] = data.get(options.get('chart_options').get('y'))

        d_legend_labels = [v for _k, v in legend_names.items() if _k in options.get('chart_options').get('left')]
        u_legend_labels = [v for _k, v in legend_names.items() if _k not in options.get('chart_options').get('left')]

        d_color = ViewConfReader.get_color_scale(options)[:len(d_series)]
        u_color = ViewConfReader.get_color_scale(options)[-len(u_series):]

        chart.vbar_stack(
            d_series,
            x=options.get('chart_options').get('x'),
            height=self.BAR_SIZE,
            color=d_color,
            source=d_data,
            legend_label=d_legend_labels
        )

        chart.vbar_stack(
            u_series,
            x=options.get('chart_options').get('x'),
            height=self.BAR_SIZE,
            color=u_color,
            source=u_data,
            legend_label=u_legend_labels
        )

        return chart

class BarHorizontalPyramid(BarHorizontalStacked):
    ''' Class for drawing bar charts '''
    def generate_stacks(self, chart, data, series, legend_names, options):
        # Left branches
        l_series = [v for v in series if v in options.get('chart_options').get('left')]
        r_series = [v for v in series if v not in options.get('chart_options').get('left')]

        l_data = {k:[-v_item for v_item in v] for k, v in data.items() if k in l_series}
        r_data = {k:v for k, v in data.items() if k in r_series}

        # Getting minimum value
        chart.x_range.start = min([min(v) for _k, v in l_data.items()])

        # Adding categories column
        l_data[options.get('chart_options').get('y')] = data.get(options.get('chart_options').get('y'))
        r_data[options.get('chart_options').get('y')] = data.get(options.get('chart_options').get('y'))

        l_legend_labels = [v for _k, v in legend_names.items() if _k in options.get('chart_options').get('left')]
        r_legend_labels = [v for _k, v in legend_names.items() if _k not in options.get('chart_options').get('left')]

        l_color = ViewConfReader.get_color_scale(options)[:len(l_series)]
        r_color = ViewConfReader.get_color_scale(options)[-len(r_series):]

        chart.hbar_stack(
            l_series,
            y=options.get('chart_options').get('y'),
            height=self.BAR_SIZE,
            color=l_color,
            source=l_data,
            legend_label=l_legend_labels
        )

        chart.hbar_stack(
            r_series,
            y=options.get('chart_options').get('y'),
            height=self.BAR_SIZE,
            color=r_color,
            source=r_data,
            legend_label=r_legend_labels
        )

        return chart
