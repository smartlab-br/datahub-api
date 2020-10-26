''' Basic chart classes and methods '''
import pandas as pd
from service.viewconf_reader import ViewConfReader

class BaseChart():
    ''' Base Chart class '''
    def __init__(self, options, dataframe, mixed_type):
        self.options = options
        self.dataframe = dataframe
        self.mixed_type = mixed_type

    @staticmethod
    def get_fill_color(index, options):
        ''' Gets the positional color in the scale built according to given options '''
        return ViewConfReader.get_color_scale(options)[index]

    @staticmethod
    def get_legend_names(dataframe, options):
        ''' Get series' names that should be plotted in legend '''
        if (options is None or options.get('chart_options', {}).get('id') is None or
                dataframe is None or dataframe.empty):
            return {}
        if options.get('chart_options', {}).get('legend_field') in dataframe.columns:
            id_field = options.get('chart_options').get('id')
            legend_field = options.get('chart_options').get('legend_field')
            tmp = dataframe[[id_field, legend_field]].drop_duplicates().to_dict(orient="records")
            return {
                item.get(id_field): item.get(legend_field)
                for
                item
                in
                tmp
            }
        return {i: i for i in dataframe[options.get('chart_options').get('id')].unique()}

    @staticmethod
    def build_tooltip(options):
        ''' Builds the tooltip HTML based on given options '''
        if options is None or 'headers' not in options:
            return 'Tooltip!'
        rows = [f'<tr style="text-align: left;"><th style="padding: 4px; padding-right: 10px;">{hdr.get("text")}</th><td style="padding: 4px;">@{hdr.get("value")}</td></tr>' for hdr in options.get('headers')]
        return f"<table>{''.join(rows)}</table>"

class BaseCartesianChart(BaseChart):
    ''' Base Cartesian Chart class '''
    @staticmethod
    def pivot_dataframe(dataframe, options):
        ''' Pivot dataframe to create series in charts '''
        if options is None:
            return None
        if dataframe is None:
            return {}
        src = dataframe.copy()
        src = pd.pivot_table(
            src,
            values=[options.get('chart_options').get('y')],
            columns=options.get('chart_options').get('id'),
            index=options.get('chart_options').get('x'),
            aggfunc="sum",
            fill_value=0
        )
        src.columns = src.columns.droplevel()
        src = src.reset_index()
        x_field = options.get('chart_options').get('x')
        src[x_field] = src[x_field].astype(str)
        return {col:list(src[col]) for col in src.columns}

    @staticmethod
    def chart_config(chart):
        ''' Adds common chart configurations, according to given options '''
        # General config
        chart.axis.major_label_text_font = 'Palanquin'
        chart.axis.major_tick_line_color = None
        chart.axis.minor_tick_line_color = None

        # Removing grid lines
        chart.xgrid.grid_line_color = None
        chart.ygrid.grid_line_color = None

        # Legend config
        chart.legend.label_text_font = 'Palanquin'
        chart.legend.location = "top_right"
        chart.legend.orientation = "vertical"

        return chart
