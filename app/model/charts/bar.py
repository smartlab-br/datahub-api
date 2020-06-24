''' Class for drawing bar charts '''
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange, VBar, HBar
from bokeh.transform import factor_cmap
from bokeh.transform import dodge
import pandas as pd
from service.viewconf_reader import ViewConfReader

class Bar():
    ''' Class for drawing bar charts '''
    BAR_SIZE = 0.8

    # TODO 1 - Population pyramid (uses stacked horizontal - check calcs to implement)
    # TODO 2 - Time series (moving bars)

    # TODO Style 1 - Add text to bar
    #     chart_options:
    #       text: "vl_indicador"

    # TODO Style 2 - Set fonts
    # TODO Style 3 - Light/Dark chart config
    # TODO Style 4 - Add CSS

    # TODO Final - Responsivity

    def draw(self, dataframe, options):
        ''' Abstract method - must be implemented '''
        raise NotImplementedError
    
    def chart_config(self, chart, options):
        # General config
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
    
class BarVertical(Bar):
    ''' Class for drawing bar charts '''
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
            src[options.get('chart_options').get('x')] = src[options.get('chart_options').get('x')].astype(str)
            data = {col:list(src[col]) for col in src.columns}
            
            # Chart initial setup
            chart = figure(x_range=data.get(options.get('chart_options').get('x')))
            chart.y_range.start = 0
            chart = self.chart_config(chart, options)

            # Create bars
            bar_width = self.BAR_SIZE / len(series)
            pos = -self.BAR_SIZE / 2
            
            for index, serie in enumerate(series):
                chart.vbar(
                    x=dodge(
                        options.get('chart_options').get('x'),
                        pos,
                        range=chart.x_range
                    ),
                    top=serie, 
                    width=bar_width - 0.05,
                    source=ColumnDataSource(data=data),
                    color=self.get_fill_color(index, options),
                    legend_label=legend_names.get(serie)
                )
                pos = pos + bar_width
        else:
            chart = figure(x_range=sorted(list(dataframe[options.get('chart_options', {}).get('x')])))
            chart.y_range.start = 0
            chart.vbar(
                x=list(dataframe[options.get('chart_options', {}).get('x')]),
                top=list(dataframe[options.get('chart_options', {}).get('y')]),
                width=self.BAR_SIZE
            )
            
        return chart

class BarHorizontal(Bar):
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

            # Create bars
            bar_width = self.BAR_SIZE / len(series)
            pos = -self.BAR_SIZE / 2

            for index, serie in enumerate(series):
                chart.hbar(
                    y=dodge(
                        options.get('chart_options').get('y'),
                        pos,
                        range=chart.y_range
                    ),
                    right=serie, 
                    height=bar_width - 0.05,
                    source=ColumnDataSource(data=data),
                    color=self.get_fill_color(index, options),
                    legend_label=legend_names.get(serie)
                )
                pos = pos + bar_width
        else:
            chart = figure(y_range=sorted(list(dataframe[options.get('chart_options', {}).get('x')])))
            chart.x_range.start = 0
            chart.hbar(
                y=list(dataframe[options.get('chart_options', {}).get('y')]),
                right=list(dataframe[options.get('chart_options', {}).get('x')]),
                width=self.BAR_SIZE
            )

        return chart

class BarVerticalStacked(Bar):
    ''' Class for drawing bar charts '''
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
            src[options.get('chart_options').get('x')] = src[options.get('chart_options').get('x')].astype(str)
            data = {col:list(src[col]) for col in src.columns}
            
            # Chart initial setup
            chart = figure(x_range=data.get(options.get('chart_options').get('x')))
            chart.y_range.start = 0
            chart = self.chart_config(chart, options)

            # Create bars
            chart.vbar_stack(
                series,
                x=options.get('chart_options').get('x'),
                width=self.BAR_SIZE, 
                color=ViewConfReader.get_color_scale(options),
                source=data,
                legend_label=[v for _k, v in legend_names.items()]
            )
        else:
            chart = figure(x_range=sorted(list(dataframe[options.get('chart_options', {}).get('x')])))
            chart.y_range.start = 0
            chart.vbar(
                x=list(dataframe[options.get('chart_options', {}).get('x')]),
                top=list(dataframe[options.get('chart_options', {}).get('y')]),
                width=self.BAR_SIZE
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

            # Create bars
            chart.hbar_stack(
                series,
                y=options.get('chart_options').get('y'),
                height=self.BAR_SIZE, 
                color=ViewConfReader.get_color_scale(options),
                source=data,
                legend_label=[v for _k, v in legend_names.items()]
            )
        else:
            chart = figure(y_range=sorted(list(dataframe[options.get('chart_options', {}).get('x')])))
            chart.x_range.start = 0
            chart.hbar(
                y=list(dataframe[options.get('chart_options', {}).get('y')]),
                right=list(dataframe[options.get('chart_options', {}).get('x')]),
                width=self.BAR_SIZE
            )

        return chart

    # SST > perfilCasosAcidentes > cat_piramide_idade_sexo
    #     api: 
    #       template: "/sst/cats?categorias=idade_cat,cd_tipo_sexo_empregado_cat&agregacao=count&filtros=eq-cd_municipio_ibge_dv-{0},and,ne-cd_tipo_sexo_empregado_cat-'Não informado',and,ne-idade_cat-0"
    #       args:
    #         - named_prop: "idLocalidade"
    #       options:
    #         calcs:
    #           - id: 'agr_count'
    #             function: 'oppose' <-- code this function to get negative values
    #             fn_args:
    #               - fixed: 'cd_tipo_sexo_empregado_cat'
    #               - fixed: 'Feminino'
    #               - fixed: 'agr_count'
    #           - id: 'agr_count_abs' <-- code this function to get absolute values
    #             function: 'absolute'
    #             fn_args:
    #               - fixed: 'calc_agr_count'
    #           - id: 'faixa_etaria' <-- code this function to bin the data
    #             function: 'get_faixa_etaria'
    #             fn_args:
    #               - fixed: 'idade_cat'
    #           - id: 'faixa_etaria_bin' <-- code this function to bin the data
    #             function: 'get_bin_faixa_etaria'
    #             fn_args:
    #               - fixed: 'idade_cat'
    #     headers:
    #       - text: 'Sexo'
    #         align: 'left'
    #         value: 'cd_tipo_sexo_empregado_cat'
    #       - text: 'Faixa etária'
    #         align: 'left'
    #         value: 'calc_faixa_etaria'
    #       - text: 'Qtde'
    #         value: 'calc_agr_count_abs'
    #     chart_options:
    #       id: "cd_tipo_sexo_empregado_cat"
    #       x: "calc_agr_count"
    #       y: "calc_faixa_etaria_bin"
    #       text: "calc_faixa_etaria"
    #       orientation: "horizontal"
    #       hide_legend: false
    #       legend_field: "cd_tipo_sexo_empregado_cat"
    #       stacked: true
    #       show_x_axis: false
   