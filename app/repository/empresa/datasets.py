''' Repository para recuperar informações de uma empresa '''
from repository.base import RedisRepository


#pylint: disable=R0903
class DatasetsRepository(RedisRepository):
    ''' Definição do repo '''
    # TODO Voltar para o nome correto
    REDIS_KEY = 'rx_new:ds'
    DATASETS = {
        'rais': ','.join([str(ano) for ano in range(2019, 2008, -1)]),
        'rfb': '2018',
        'sisben': ','.join([str(ano) for ano in range(2020, 2017, -1)]),
        'catweb': ','.join([str(ano) for ano in range(2020, 2010, -1)]),
        'auto': ','.join([str(ano) for ano in range(2019, 2001, -1)]),
        'caged': ','.join([
            '{:d}{:02d}'.format(ano, mes)
            for ano in range(2020, 2008, -1)
            for mes in range(12, 0, -1)
            if not (ano == 2020 and mes > 8)
        ]),
        'cagedsaldo': ','.join([
            '{:d}{:02d}'.format(ano, mes)
            for ano in range(2020, 2008, -1)
            for mes in range(12, 0, -1)
            if not (ano == 2020 and mes > 8)
        ]),
        'cagedtrabalhador': ','.join([
            '{:d}{:02d}'.format(ano, mes)
            for ano in range(2020, 2002, -1)
            for mes in range(12, 0, -1)
            if not (ano == 2020 and mes > 8)
        ]),
        'cagedtrabalhadorano': ','.join([str(ano) for ano in range(2020, 2002, -1)]),
        'rfbsocios': '2018',
        'rfbparticipacaosocietaria': '2018',
        'renavam': '2018',
        'aeronaves': '2018'
    }


    # NA - para as bases marcadas com NA falar com Lucas para criarmos uma coluna de data da base de dados (data de extração no órgão de origem) Temos algo do tipo ?
    DATASETS_COMPETENCIA = {
        "auto": "DISTINCT ano",
        "caged": "DISTINCT ano",
        "cagedano": "DISTINCT ano",
        "cagedsaldo": "DISTINCT competencia_mov",
        "cagedtrabalhador": "DISTINCT competencia_mov",
        "cagedtrabalhadorano": "DISTINCT ano_declarado",
        "rais": "DISTINCT nu_ano_rais",
        "catweb_c": "DISTINCT ano",
        "catweb": "DISTINCT ano_cat",
        "rfb": "MAX dt_carga",
        "sisben_c": "DISTINCT nu_ano_compet",
        "sisben": "DISTINCT ano_beneficio",
        "rfbsocios": "MAX dt_carga",
        "rfbparticipacaosocietaria": "MAX dt_carga",
        "renavam": "MAX dt_carga",
        "aeronaves": "MAX dt_carga"
    }


    def retrieve(self):
        ''' Localiza o dicionário de datasources no REDIS '''
        return self.retrieve_hashset(self.REDIS_KEY)

    def store(self, datasets):
        ''' Inclui/atualiza dicionário de competências e datasources no REDIS '''
        # self.get_dao().hmset(self.REDIS_KEY, self.DATASETS)
        self.get_dao().hmset(self.REDIS_KEY, datasets)

        return datasets
