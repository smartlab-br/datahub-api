''' Class for drawing bar charts '''
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange, VBar, HBar
from bokeh.transform import factor_cmap
import pandas as pd
from service.viewconf_reader import ViewConfReader

class Bar():
    ''' Class for drawing bar charts '''
    BAR_SIZE = 0.8

    def draw(self, dataframe, options):
        ''' Draw a bar chart according to given options '''
        # http://localhost:5000/charts/bar?from_viewconf=S&au=2927408&card_id=bar_serie_resgate&dimension=prevalencia&observatory=te&as_image=N
        print(options)
        # TODO 1 - Add text to bar
        # TODO 1 - Add CSS

        # TODO 2 - Time series (moving bars)
        # TODO 4 - Stacked
        # TODO 5 - Population pyramid

        # TODO Final - Responsivity

        # TODO - [REMOVE] Options for color testing
        options.get('chart_options')["colorArray"] = ["#FF0000", "blue", "green"]

        # TODO - [REMOVE] Options for horizontal bars
        options.get('chart_options')['y'] = "nu_competencia"
        options.get('chart_options')['x'] = "vl_indicador"
        options.get('chart_options')['orientation'] = "horizontal"                         
        options.get('chart_options')['show_x_axis'] = False
        options.get('chart_options')['show_y_axis'] = True

        # TODO - [REMOVE] Options for stacked bars
        options.get('chart_options')['stacked'] = True

        series = None
        if options.get('chart_options', {}).get('id'):
            series = sorted(dataframe[options.get('chart_options', {}).get('id')].unique())
    
        (source, chart) = self.get_figure(dataframe, options)

        if list(series):
            palette = ViewConfReader.get_color_scale(options)
            if options.get('chart_options', {}).get('orientation', 'horizontal') == 'vertical':
                glyph = VBar(
                    x="axis",
                    top="vals",
                    width = self.BAR_SIZE,
                    fill_color = factor_cmap(
                        'axis',
                        palette=palette,
                        factors=series,
                        start=1,
                        end=len(palette)
                    )
                )
            else:
                glyph = HBar(
                    y="axis",
                    right="vals",
                    left=0,
                    height = self.BAR_SIZE,
                    fill_color = factor_cmap(
                        'axis',
                        palette=palette,
                        factors=series,
                        start=1,
                        end=len(palette)
                    )
                )
        else:
            glyph = VBar(x="axis", top="vals", width = self.BAR_SIZE)

        chart.add_glyph(source, glyph)

        return chart

    def get_figure(self, dataframe, options):
        if options.get('chart_options', {}).get('orientation', 'horizontal') == 'vertical':
            if options.get('chart_options', {}).get('id'):
                axis = [(str(row[options.get('chart_options', {}).get('x')]), row[options.get('chart_options', {}).get('id')]) for _row_id, row in dataframe.iterrows()]
            else:
                axis = [str(row[options.get('chart_options', {}).get('x')]) for _row_id, row in dataframe.iterrows()]
            chart = figure(x_range=FactorRange(*axis))
            chart.y_range.start = 0
        else:
            if options.get('chart_options', {}).get('id'):
                axis = [(str(row[options.get('chart_options', {}).get('y')]), row[options.get('chart_options', {}).get('id')]) for _row_id, row in dataframe.iterrows()]
            else:
                axis = [str(row[options.get('chart_options', {}).get('y')]) for _row_id, row in dataframe.iterrows()]    
            chart = figure(y_range=FactorRange(*axis))
        
        source = ColumnDataSource(
            data=dict(
                axis=axis,
                vals=list(dataframe['vl_indicador'])
            )
        )
        
        # General config
        chart.axis.major_tick_line_color = None
        chart.axis.minor_tick_line_color = None
        chart.axis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
        chart.axis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
        
        # Removing grid lines
        chart.xgrid.grid_line_color = None
        chart.ygrid.grid_line_color = None

        # Axis visibility
        if not options.get('chart_options', {}).get('show_x_axis', False):
            chart.xaxis.visible = False
        if not options.get('chart_options', {}).get('show_y_axis', False):
            chart.yaxis.visible = False

        return (source, chart)

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
