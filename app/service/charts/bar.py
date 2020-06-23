''' Class for drawing bar charts '''
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange, VBar
from bokeh.transform import factor_cmap
import pandas as pd

class Bar():
    ''' Class for drawing bar charts '''
    BAR_WIDTH = 0.8

    def draw(self, dataframe, options):
        ''' Draw a bar chart according to given options '''
        # http://localhost:5000/charts/bar?from_viewconf=S&au=2927408&card_id=bar_serie_resgate&dimension=prevalencia&observatory=te&as_image=N
        print(options)
        # TODO 1 - Add Colors
        # TODO 1 - Add text to bar
        # TODO 1 - Add CSS

        # TODO 2 - Time series
        # TODO 3 - Horizontal
        # TODO 4 - Stacked
        # TODO 5 - Population pyramid

        # TODO - [REMOVE] Options for color testing
        options.get('chart_options')["colorArray"] = ["#FF0000", "blue", "green"]
        series = None
        if options.get('chart_options', {}).get('id'):
            series = dataframe[options.get('chart_options', {}).get('id')].unique()

        if options.get('chart_options', {}).get('id'):
            x = [(str(row[options.get('chart_options', {}).get('x')]), row[options.get('chart_options', {}).get('id')]) for _row_id, row in dataframe.iterrows()]
        else:
            x = [str(row[options.get('chart_options', {}).get('x')]) for _row_id, row in dataframe.iterrows()]
            
        source = ColumnDataSource(data=dict(
            x=x,
            vals=list(dataframe['vl_indicador'])
        ))
        
        chart = figure(x_range=FactorRange(*x))

        # General config
        chart.y_range.start = 0
        chart.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
        chart.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
        chart.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
        chart.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
        chart.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
        chart.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
        
        # Removing grid lines
        chart.xgrid.grid_line_color = None
        chart.ygrid.grid_line_color = None

        # Axis visibility
        if not options.get('chart_options', {}).get('show_x_axis', False):
            chart.xaxis.visible = False
        if not options.get('chart_options', {}).get('show_y_axis', False):
            chart.yaxis.visible = False

        # chart.vbar(
        #     x='x', 
        #     top='vals', 
        #     width=0.9, 
        #     source=source
        #     # fill_color=self.get_palette(options.get('chart_options'))
        # )

        if list(series):
            glyph = VBar(
                x="x",
                top="vals",
                width = self.BAR_WIDTH,
                fill_color = factor_cmap(
                    'x',
                    palette=self.get_palette(options.get('chart_options')),
                    factors=series,
                    # start=1,
                    end=3
                )
            )
        else:
            glyph = VBar(
                x="x",
                top="vals",
                width = self.BAR_WIDTH
            )

        chart.add_glyph(source, glyph)

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
        #       orientation: "vertical"                         
        #       legend_field: "calc_ds_indicador_radical"      
        #       show_x_axis: true                               OK    
        #       show_y_axis: false                              OK
        #     source:
        #       desc: "Bancos de dados do Seguro-Desemprego do Trabalhador Resgatado, do Sistema de Acompanhamento do Trabalho Escravo (SISACTE) e do Sistema COETE (Controle de Erradicação do Trabalho Escravo), referentes ao período iniciado em 2003 (Primeiro Plano Nacional de Erradicação do Trabalho Escravo). Os dados brutos foram fornecidos pelo Ministério da Economia do Brasil."
        #       link: ""
    def get_palette(self, options):
        return tuple(options.get('colorArray'))