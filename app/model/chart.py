''' Model for fetching chart '''
import io
from html.parser import HTMLParser
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.io.export import get_screenshot_as_png
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from model.base import BaseModel
from model.thematic import Thematic
from service.viewconf_reader import ViewConfReader
from factory.chart import ChartFactory

class Chart(BaseModel):
    ''' Model for fetching dinamic and static charts '''
    CHART_LIB_DEF = {
        'FOLIUM': ['MAP_TOPOJSON', 'MAP_HEAT', 'MAP_CLUSTER', 'MAP_BUBBLES', 'MIXED_MAP']
    } # Defaults to BOKEH
    def get_chart(self, options):
        ''' Selects if the chart should be static or dynamic '''
        mixed_type = None
        as_image = options.get('as_image')
        options['as_pandas'] = True
        options['no_wrap'] = True

        if options.get('from_viewconf'):
            added_options = ViewConfReader.set_custom_options(options)
            struct = ViewConfReader().get_card_descriptor(
                options.get('language', 'br'),
                options.get('observatory', 'td'),
                options.get('scope', 'municipio'),
                options.get('dimension'),
                options.get('card_id')
            )
            # TODO - [REMOVE] Testing heatmap with time series
            # struct['api']['template'] = "/te/indicadoresmunicipais?"
            # "categorias=latitude,nu_competencia,longitude,cd_mun_ibge,nm_municipio,cd_indicador&"
            # "valor=vl_indicador&agregacao=sum&"
            # "filtros=nn-vl_indicador,and,in-cd_indicador-'te_rgt'-'te_nat'-'te_res',"
            # "and,eq-cd_uf-{0}&calcs=ln_norm_pos_part"
            # struct['chart_options']['timeseries'] = 'nu_competencia'

            # TODO - [REMOVE] Testing bubbles with time series
            # struct['api']['template'] = "/te/indicadoresmunicipais?"
            # "categorias=latitude,longitude,cd_mun_ibge,nm_municipio,nu_competencia,cd_indicador&"
            # "valor=vl_indicador&agregacao=sum&"
            # "filtros=nn-vl_indicador,and,in-cd_indicador-'te_rgt'-'te_nat'-'te_res',"
            # "and,eq-cd_uf-{0}&calcs=ln_norm_pos_part"
            # struct['chart_options']['timeseries'] = 'nu_competencia'

            # TODO - [REMOVE] Testing pyramid with cut
            # struct['api']['template'] = "/sst/cats/cut-idade_cat?"
            # "categorias=idade_cat,cd_tipo_sexo_empregado_cat&"
            # "agregacao=count&"
            # "filtros=eq-cd_municipio_ibge_dv-{0},and,"
            # "ne-cd_tipo_sexo_empregado_cat-'Não informado',and,ne-idade_cat-0"

            if struct.get('chart_type') == 'MIXED_MAP':
                mixed_type = struct.get('chart_type')
                dataframe = []
                nu_options = []
                for layer in struct.get('chart_options').get('layers'):
                    curr_options = {
                        **options,
                        **struct,
                        **ViewConfReader.api_to_options(
                            layer.get('api'),
                            {**layer, **added_options}
                        ),
                        **layer
                    }

                    nu_options.append(curr_options)

                    each_df = self.get_dataframe({}, curr_options, added_options)
                    each_df = ViewConfReader().generate_columns(each_df, curr_options)
                    dataframe.append(each_df)
                options = nu_options
            else:
                added_options = ViewConfReader.set_custom_options(options)
                options = {
                    **options,
                    **ViewConfReader.api_to_options(
                        struct.get('api'),
                        {**options, **added_options}
                    ),
                    **struct
                }
                dataframe = self.get_dataframe(options, struct, added_options)
                # Runs dataframe modifiers from viewconf
                dataframe = ViewConfReader().generate_columns(dataframe, options)
        elif options.get('chart_type') == 'MIXED_MAP':
            mixed_type = options.get('chart_type')
            dataframe = []
            for each_options in options.get('chart_options').get('layers'):
                added_options = ViewConfReader.set_custom_options(each_options)
                curr_options = {
                    **each_options,
                    **ViewConfReader.api_to_options(
                        each_options.get('api'),
                        {**options, **added_options}
                    ),
                }

                each_df = self.get_dataframe({}, curr_options, added_options)
                # Runs dataframe modifiers from viewconf
                each_df = ViewConfReader().generate_columns(each_df, curr_options)
                dataframe.append(each_df)
            options = options.get('chart_options').get('layers')
        else:
            added_options = ViewConfReader.set_custom_options(options)
            options = {
                **options,
                **ViewConfReader.api_to_options(
                    options.get('api'),
                    {**options, **added_options}
                ),
            }
            dataframe = self.get_dataframe({}, options, added_options)
            # Runs dataframe modifiers from viewconf
            dataframe = ViewConfReader().generate_columns(dataframe, options)

        chart = ChartFactory().create(options, dataframe, mixed_type).draw()

        chart_lib = 'BOKEH'
        chart_type = mixed_type
        if chart_type is None:
            chart_type = options.get('chart_type')

        for chart_key, chart_types in self.CHART_LIB_DEF.items():
            if chart_type in chart_types:
                chart_lib = chart_key

        if as_image:
            return self.get_image(chart, chart_lib)
        return self.get_dynamic_chart(chart, chart_lib)

    @staticmethod
    def get_image(chart, lib):
        ''' Gets chart as image '''
        if lib == 'BOKEH':
            img = get_screenshot_as_png(chart)
            roi_img = img.crop()
            img_byte_array = io.BytesIO()

            roi_img.save(img_byte_array, format='PNG')
            return img_byte_array.getvalue()
        if lib == 'FOLIUM':
            ff_options = Options()
            ff_options.set_headless(headless=True)

            cap = DesiredCapabilities().FIREFOX
            cap["marionette"] = True
            driver = webdriver.Firefox(firefox_options=ff_options, capabilities=cap)

            driver.get(
                "data:text/html;charset=utf-8,{html_content}".format(
                    html_content=chart._repr_html_()
                )
            )

            return driver.get_screenshot_as_png()
        return None

    @staticmethod
    def get_dynamic_chart(chart, lib):
        ''' Gets dynamic chart '''
        # /charts?theme=teindicadoresmunicipais&categorias=ds_agreg_primaria&
        # valor=vl_indicador&agregacao=SUM&filtros=eq-cd_mun_ibge-2927408,and,
        # eq-cd_indicador-%27te_nat_ocup_atual%27
        if lib == 'BOKEH':
            (script, div) = components(chart)
            return {
                'script': HTMLParser().unescape(script),
                'div': HTMLParser().unescape(div)
            }
        if lib == 'FOLIUM':
            # from bs4 import BeautifulSoup
            # import base64
            # soup = BeautifulSoup(chart._repr_html_(), 'html.parser')
            # content = soup.find_all('iframe')[0]['data-html'].encode('ascii')
            # content = base64.b64decode(content).decode('ascii')
            # return {'div': content, 'mime': 'text/html'}
            return {'div': chart._repr_html_(), 'mime': 'text/html'}
        return None

    def get_dataframe(self, options, struct={}, added_options={}):
        if options.get('operation'):
            return Thematic().find_and_operate(
                options.get('operation'),
                {
                    **{'as_pandas': True, 'no_wrap': True},
                    **ViewConfReader.api_to_options(
                        struct.get('api'),
                        {**options, **added_options}
                    )
                }
            )
        return Thematic().find_dataset(
            {
                **{'as_pandas': True, 'no_wrap': True},
                **ViewConfReader.api_to_options(
                    struct.get('api'),
                    {**options, **added_options}
                )
            }
        )

    @staticmethod
    def draw_scatter(dataframe, _options):
        ''' Draws the scatterplot '''
        # http://localhost:5000/charts/scatter?theme=sstindicadoresestaduais&categorias=ds_agreg_primaria-v,ds_agreg_secundaria-x,vl_indicador-y&filtros=eq-nu_competencia-2017,and,eq-cd_indicador-%27sst_bene_sexo_idade_dias_perdidos%27&as_image=S
        colormap = {'Feminino': 'red', 'Masculino': 'blue', 'Indefinido': 'pink'}
        chart = figure()
        chart.circle(
            dataframe["x"], dataframe["y"],
            color=[colormap[x] for x in dataframe['v']],
            fill_alpha=0.2, size=10
        )

        # output_file("iris.html", title="iris.py example")
        return chart
