""" Repository para recuperar informações da CEE """
from datetime import datetime
from model.thematic import Thematic


# pylint: disable=R0903
class AcidentometrosSST(Thematic):
    """ Definição do repo """
    METADATA = {
        'fonte': 'SMARTLAB', 'link': 'http://smartlab.mpt.mp.br/'
    }

    # TODO - Check attributes for dynamic lookups
    THEMATIC_LOOKUPS = [
        {
            "theme": "sstindicadoresnacionais",
            "categorias": ["cd_indicador", "ds_indicador", "nu_competencia_min", "nu_competencia_max"],
            "valor": ["vl_indicador"],
            "where": ["in-cd_indicador-'sst_cat_obito'-'sst_cat_total'-'sst_bene_dias_perdidos_91'-'sst_bene_despesa'"],
            "agregacao": ["SUM"],
            "no_wrap": True
        },
        {
            "theme": "indicadoresnacionais",
            "categorias": ["cd_indicador", "ds_indicador", "nu_competencia_min", "nu_competencia_max"],
            "valor": ["vl_indicador"],
            "where": ["in-cd_indicador-'06_05_10_00'"],
            "agregacao": ["SUM"],
            "no_wrap": True
        }
    ]

    def obter_acidentometros(self):
        """ Prepara os dados dos acidentômetros para resposta """
        dataframe = None
        for lookup in self.THEMATIC_LOOKUPS:
            if dataframe is None:
                dataframe = self.find_dataset(lookup)
                continue
            dataframe = dataframe.append(self.find_dataset(lookup))
        dataframe.rename(columns={"agr_sum_vl_indicador": "vl_indicador"}, inplace=True)

        # Ajusta valor de indicador para número oficial
        # Gastos da previdência:
        # HC - 66.534.254.002    (Esse valor substitui qualquer valor vindo do dataset) - 2017
        # HC - 79.000.041.558,11 (Esse valor substitui qualquer valor vindo do dataset) - 2018
        # HC - 92.397.552.855,30 (Esse valor substitui qualquer valor vindo do dataset) - 2019
        # HC - 106.097.737.197,64 (Esse valor substitui qualquer valor vindo do dataset) - 2020
        # HC - 120.604.942.559,81 (Esse valor substitui qualquer valor vindo do dataset) - 2021
        dataframe.loc[dataframe['cd_indicador'] == 'sst_bene_despesa', ['vl_indicador']] = 120604942559.81
        # Momento atual, em milissegundos
        dataframe['momento_ms'] = int(round(datetime.now().timestamp() * 1000))
        # Início e final do período medido, em milissegundos
        dataframe['nu_competencia_min_ms'] = dataframe['nu_competencia_min'].apply(
            lambda x: self.obter_ms_from_year(x, 'min'))
        dataframe['nu_competencia_max_ms'] = dataframe['nu_competencia_max'].apply(
            lambda x: self.obter_ms_from_year(x, 'max'))
        # Passo da atualização (incremento de valor por milissegundo)
        dataframe['delta_por_ms'] = dataframe['vl_indicador'] / (dataframe['nu_competencia_max_ms'] - dataframe['nu_competencia_min_ms'])
        # Valor estimado
        dataframe['vl_estimado'] = dataframe['vl_indicador'] + (dataframe['momento_ms'] - dataframe['nu_competencia_max_ms']) * dataframe['delta_por_ms']
        return dataframe.to_json(orient="records")

    @staticmethod
    def obter_ms_from_year(year, min_max='max'):
        """ Gets millis from an year's end or start """
        end_str = "-12-31 23:59:59.999999"
        if min_max == 'min':
            end_str = "-01-01 00:00:00.000000"
        return int(round(datetime.strptime(str(year) + end_str, "%Y-%m-%d %H:%M:%S.%f").timestamp() * 1000))
