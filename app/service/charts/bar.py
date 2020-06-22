''' Class for drawing bar charts '''
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange
import pandas as pd

class Bar():
    ''' Class for drawing bar charts '''

    def draw(self, dataframe, options):
        ''' Draw a bar chart according to given options '''
        # http://localhost:5000/charts/bar?from_viewconf=S&au=2927408&card_id=bar_serie_resgate&dimension=prevalencia&observatory=te&as_image=N
        print(options)
        # colormap = {'Feminino': 'red', 'Masculino': 'blue', 'Indefinido': 'pink'}
        x = [(str(row['nu_competencia']), row['cd_indicador']) for _row_id, row in dataframe.iterrows()]
        source = ColumnDataSource(data=dict(
            x=x,
            vals=list(dataframe['vl_indicador'])
        ))
        
        chart = figure(
            x_range=FactorRange(*x),
            plot_height=250,
            title="Fruit Counts by Year",
            toolbar_location=None,
            tools=""
        )

        chart.vbar(x='x', top='vals', width=0.9, source=source)

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
        #     template: "{0}, de {1} a {2}"
        #     api: 
        #         fixed: "/te/indicadoresnacionais?categorias=nu_competencia_min,nu_competencia_max&limit=1&filtros=eq-cd_indicador-'te_nat'"
        #     args:
        #         - base_object: "localidade"
        #         named_prop: "nm_localidade"
        #         - named_prop: "nu_competencia_min"
        #         - named_prop: "nu_competencia_max"
        #     description:
        #     - type: "text"
        #         title: ""
        #         content:
        #         fixed: "No gráfico ao lado, destaca-se a série histórica dos registros relacionados a resgates do trabalho escravo consoante três perspectivas: resgatados na localidade, em verde; nascidos na localidade e que foram resgatados, ainda que fora da localidade em destaque; e residentes na localidade que foram resgatados, ainda que em outros locais, após possível aliciamento onde residiam à época. Essas informações permitem identificar oportunidades de melhor alocação de recursos para aprimoramento do desenvolvimento humano (nos locais de naturalidade), da prevenção do aliciamento (nos locais de residência) e da repressão (nos locais de resgate)."
        #     api:
        #     template: "/te/indicadoresmunicipais?categorias=cd_indicador,cd_mun_ibge,nu_competencia,vl_indicador&filtros=eq-cd_mun_ibge-{0},and,in-cd_indicador-'te_nat'-'te_res'-'te_rgt'"
        #     args:
        #         - named_prop: "idLocalidade"
        #     options:
        #         calcs:
        #         - id: "ds_indicador_radical"
        #             function: "get_te_label"
        #             fn_args:
        #             - fixed: "cd_indicador"
        #     headers:
        #     - text: 'Indicador'
        #         align: 'left'
        #         value: 'calc_ds_indicador_radical'
        #     - text: 'Ano'
        #         align: 'left'
        #         value: 'nu_competencia'
        #     - text: 'Quantidade'
        #         value: 'vl_indicador'
        #     chart_options:
        #     id: "cd_indicador"
        #     x: "nu_competencia"
        #     y: "vl_indicador"
        #     text: "vl_indicador"
        #     orientation: "vertical"
        #     legend_field: "calc_ds_indicador_radical"
        #     show_x_axis: true
        #     show_y_axis: false
        #     source:
        #     desc: "Bancos de dados do Seguro-Desemprego do Trabalhador Resgatado, do Sistema de Acompanhamento do Trabalho Escravo (SISACTE) e do Sistema COETE (Controle de Erradicação do Trabalho Escravo), referentes ao período iniciado em 2003 (Primeiro Plano Nacional de Erradicação do Trabalho Escravo). Os dados brutos foram fornecidos pelo Ministério da Economia do Brasil."
        #     link: ""
