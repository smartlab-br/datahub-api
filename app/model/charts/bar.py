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

    # TODO 2 - Time series (moving bars)
    # TODO 4 - Population pyramid

    # TODO Style 1 - Add text to bar
    # TODO Style 2 - Set fonts
    # TODO Style 5 - Add CSS

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
        # - id: "bar_serie_resgate"
        #     chart_type: "BAR"
        #     title:
        #     fixed: "Trabalhadores resgatados - Série Histórica"
        #     info:
        #     - type: "text"
        #         title: "Sobre a métrica"
        #         content:
        #         fixed: ""
        #     title_comment:
        #       template: "{0}, de {1} a {2}"
        #     api: 
        #         fixed: "/te/indicadoresnacionais?categorias=nu_competencia_min,nu_competencia_max&limit=1&filtros=eq-cd_indicador-'te_nat'"
        #     args:
        #       - base_object: "localidade"
        #         named_prop: "nm_localidade"
        #           - named_prop: "nu_competencia_min"
        #           - named_prop: "nu_competencia_max"
        #     description:
        #       - type: "text"
        #         title: ""
        #         content:
        #         fixed: "No gráfico ao lado, destaca-se a série histórica dos registros relacionados a resgates do trabalho escravo consoante três perspectivas: resgatados na localidade, em verde; nascidos na localidade e que foram resgatados, ainda que fora da localidade em destaque; e residentes na localidade que foram resgatados, ainda que em outros locais, após possível aliciamento onde residiam à época. Essas informações permitem identificar oportunidades de melhor alocação de recursos para aprimoramento do desenvolvimento humano (nos locais de naturalidade), da prevenção do aliciamento (nos locais de residência) e da repressão (nos locais de resgate)."
        #     api:
        #       template: "/te/indicadoresmunicipais?categorias=cd_indicador,cd_mun_ibge,nu_competencia,vl_indicador&filtros=eq-cd_mun_ibge-{0},and,in-cd_indicador-'te_nat'-'te_res'-'te_rgt'"
        #       args:
        #         - named_prop: "idLocalidade"
        #     options:
        #         calcs:
        #         - id: "ds_indicador_radical"
        #             function: "get_te_label"
        #             fn_args:
        #             - fixed: "cd_indicador"
        #     headers:
        #       - text: 'Indicador'
        #         align: 'left'
        #         value: 'calc_ds_indicador_radical'
        #       - text: 'Ano'
        #         align: 'left'
        #         value: 'nu_competencia'
        #       - text: 'Quantidade'
        #         value: 'vl_indicador'
        #     chart_options:
        #       id: "cd_indicador"                              OK
        #       x: "nu_competencia"                             OK
        #       y: "vl_indicador"                               OK
        #       text: "vl_indicador"
        #       orientation: "vertical"                         OK                      
        #       legend_field: "calc_ds_indicador_radical"       OK
        #       show_x_axis: true                               OK    
        #       show_y_axis: false                              OK
        