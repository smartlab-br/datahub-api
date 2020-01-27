''' Model for fetching chart '''
from model.base import BaseModel
from model.thematic import Thematic
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
import io

class Chart(BaseModel):
    ''' Model for fetching dinamic and static charts '''
    def get_chart(self, options):
        ''' Selects if the chart should be static or dynamic '''
        options['as_pandas'] = True
        options['no_wrap'] = True
        dataframe = Thematic().find_dataset(options)
        chart = self.get_raw_chart(dataframe, options)
        
        if options['as_image']:
            return self.get_image(chart, options)
        return self.get_dynamic_chart(chart, options)
    
    def get_raw_chart(self, dataframe, options):
        ''' Selects and loads the chart '''
        if options['chart_type'] == 'scatter':
            return self.draw_scatter(dataframe, options)
        pass
        
    def get_image(self, chart, options):
        ''' Gets chart as image '''
        # /charts?theme=teindicadoresmunicipais&categorias=ds_agreg_primaria&valor=vl_indicador&agregacao=SUM&filtros=eq-cd_mun_ibge-2927408,and,eq-cd_indicador-%27te_nat_ocup_atual%27

        # bytes_image = io.BytesIO()
        # chart.savefig(bytes_image, format='png')
        # bytes_image.seek(0)
        from bokeh.io import export_png

        bytes_image = export_png(chart, filename="chart.png")
        
        return bytes_image

    def get_dynamic_chart(self, chart, options):
        ''' Gets dynamic chart '''
        # /charts?theme=teindicadoresmunicipais&categorias=ds_agreg_primaria&valor=vl_indicador&agregacao=SUM&filtros=eq-cd_mun_ibge-2927408,and,eq-cd_indicador-%27te_nat_ocup_atual%27
        (script, div) = components(chart)
        return {'script': script, 'div': div }

    def draw_scatter(self, dataframe, options):
        ''' Draws the scatterplot '''
        # http://localhost:5000/charts/scatter?theme=sstindicadoresestaduais&categorias=ds_agreg_primaria-v,ds_agreg_secundaria-x,vl_indicador-y&filtros=eq-nu_competencia-2017,and,eq-cd_indicador-%27sst_bene_sexo_idade_dias_perdidos%27&as_image=S
        colormap = {'Feminino': 'red', 'Masculino': 'blue', 'Indefinido': 'pink'}
        chart = figure()
        chart.circle(
            dataframe["x"], dataframe["y"],
            color=[colormap[x] for x in dataframe['v']],
            fill_alpha=0.2, size=10)

        # output_file("iris.html", title="iris.py example")
        return chart
