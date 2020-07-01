''' Class for drawing bar charts '''
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange, NumeralTickFormatter
from bokeh.transform import factor_cmap
from bokeh.transform import dodge
import pandas as pd
from service.viewconf_reader import ViewConfReader
from bokeh.themes import built_in_themes
from bokeh.io import curdoc

class Line():
    ''' Class for drawing bar charts '''
    LINE_WIDTH = 4

    def __init__(self, style_theme):
        curdoc().theme = style_theme # Dark = dark_minimal

    def draw(self, dataframe, options):
        series = sorted(dataframe[options.get('chart_options', {}).get('id')].unique())
        if list(series):
            legend_names = self.get_legend_names(dataframe, options)
            
            # Pivot dataframe
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
            # src[options.get('chart_options').get('x')] = src[options.get('chart_options').get('x')].astype(str)
            # data = {col:list(src[col]) for col in src.columns}
            
            # Chart initial setup
            chart = figure()
            chart.y_range.start = dataframe[options.get('chart_options').get('y')].min()
            chart = self.chart_config(chart, options)

            for index, serie in enumerate(series):
                chart.line(
                    list(src[options.get('chart_options').get('x')]),
                    list(src[serie]),
                    line_width=self.LINE_WIDTH,
                    line_color=self.get_fill_color(index, options),
                    legend_label=legend_names.get(serie)
                )
        else:
            chart = figure()
            chart.y_range.start = dataframe[options.get('chart_options').get('y')].min()
            chart.line(
                list(dataframe[options.get('chart_options').get('x')]),
                list(dataframe[options.get('chart_options', {}).get('y')]),
                line_width=self.LINE_WIDTH
            )
            
        return chart
    
    def chart_config(self, chart, options):
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
    
    def get_fill_color(self, index, options):
        return ViewConfReader.get_color_scale(options)[index]
    
    def get_legend_names(self, dataframe, options):
        if options.get('chart_options').get('legend_field') and options.get('chart_options').get('legend_field') in dataframe.columns:
            tmp = dataframe[[options.get('chart_options').get('id'), options.get('chart_options').get('legend_field')]].drop_duplicates().set_index(options.get('chart_options').get('id')).to_dict()
            return tmp.get(options.get('chart_options').get('legend_field'))
        return {i: i for i in dataframe[options.get('chart_options').get('id')].unique()}
    
class LineArea(Line):
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
                values=[options.get('chart_options').get('y')],
                columns=options.get('chart_options').get('id'),
                index=options.get('chart_options').get('x'),
                aggfunc="sum",
                fill_value=0
            )
            src.columns = src.columns.droplevel()
            src = src.reset_index()
            src[options.get('chart_options').get('x')] = src[options.get('chart_options').get('x')].astype(str)
            data = {col:list(src[col]) for col in src.columns}
            
            # Chart initial setup
            chart = figure()
            chart.y_range.start = dataframe[options.get('chart_options').get('y')].min()
            chart = self.chart_config(chart, options)

            chart.varea_stack(
                series,
                x = options.get('chart_options').get('x'),
                color = ViewConfReader.get_color_scale(options),
                source = data
            )
        else:
            chart = figure()
            chart.y_range.start = dataframe[options.get('chart_options').get('y')].min()
            chart.line(
                list(dataframe[options.get('chart_options').get('x')]),
                list(dataframe[options.get('chart_options', {}).get('y')]),
                line_width=self.LINE_WIDTH
            )

        return chart

# chart_type: "LINE"
#     # preloaded:
#     #   prop: "centralindicadores"
#     #   function: "slice"
#     #   id: ["02_11_01_00", "02_11_02_00"]
#     api:
#         template: "/indicadoresmunicipais?categorias=cd_mun_ibge,nm_municipio,cd_dimensao,ds_indicador_radical,ds_indicador_curto,ds_agreg_primaria,cd_indicador,nu_competencia,ds_fonte,vl_indicador,media_uf,pct_uf,rank_uf,rank_br,latitude,longitude&filtros=eq-cd_mun_ibge-{0},and,in-cd_indicador-'02_11_01_00'-'02_11_02_00',and,le-nu_competencia-nu_competencia_max&ordenacao=cd_indicador"
#         args:
#           - named_prop: "idLocalidade"
#         options:
#         formatters:
#             - id: "vl_indicador"
#               format: 'inteiro'
#     headers:
#         - text: 'Indicador'
#           align: 'left'
#           value: 'ds_indicador_radical'
#         - text: 'Ano'
#           align: 'left'
#           value: 'nu_competencia'
#         - text: 'Quantidade'
#           value: 'fmt_vl_indicador'
#     chart_options:
#         id: "cd_indicador"
#         x: "nu_competencia"
#         y: "vl_indicador"
#         hide_legend: false
#         legend_field: "ds_agreg_primaria"
#         colorArray: ["#377EB8","#E41A1C"]  # blue / red