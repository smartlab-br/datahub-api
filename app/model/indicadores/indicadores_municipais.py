''' Repository para recuperar informações da CEE '''
from model.base import BaseModel
from repository.indicadores.indicadores_municipais import IndicadoresMunicipaisRepository

#pylint: disable=R0903
class IndicadoresMunicipais(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'IBGE', 'link': 'http://ibge.gov.br/'
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = IndicadoresMunicipaisRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = IndicadoresMunicipaisRepository()
        return self.repo

    def load_chart(self, options):
        ''' Draws the chart according to the options provided '''
        options['no_wrap'] = True
        dataset = self.find_dataset(options)

        # Histogram test
        from bokeh.charts import Histogram
        from bokeh.embed import file_html

        p = Histogram(dataset, values='vl_indicador', color='navy', title="Teste")

        return file_html(p, (None, None))
