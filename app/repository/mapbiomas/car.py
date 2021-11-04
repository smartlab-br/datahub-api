''' Repository para recuperar informações da CEE '''
import pandas as pd
from repository.base import ImpalaRepository, RedisRepository
from datetime import datetime

#pylint: disable=R0903
class CarRepository(ImpalaRepository):
    ''' Definição do repo '''
    TABLE_NAMES = {
        'MAIN': 'car'
    }
    PAGE_SIZE = 200
    NAMED_QUERIES = {
        'QRY_FIND_DATASET': 'SELECT {} FROM {} {} {} {} {} {}',
        'QRY_FIND_BY_CODE': '''SELECT 
            car_code AS carCode, nm_proprietarios, cpf_cnpj_proprietarios,
            nm_imovel, alertcode, CAST(alertinsertedat AS STRING) as alertinsertedat, areaha,
            coordinates, CAST(detectedat AS STRING) as detectedat, geometry, id, source,
            statusid, car_id, CAST(statusinsertedat AS STRING) as statusinsertedat
            FROM private.mapbiomas_alerta WHERE car_code = "{}"
            ORDER BY detectedat DESC, areaha DESC
            LIMIT {} OFFSET {}''',
        'QRY_FIND_BY_CODES': '''SELECT 
            car_code AS carCode, nm_proprietarios, cpf_cnpj_proprietarios,
            nm_imovel, alertcode, CAST(alertinsertedat AS STRING) as alertinsertedat, areaha,
            coordinates, CAST(detectedat AS STRING) as detectedat, geometry, id, source,
            statusid, car_id, CAST(statusinsertedat AS STRING) statusinsertedat
            FROM private.mapbiomas_alerta WHERE car_code IN ({})
            ORDER BY detectedat DESC, areaha DESC
            LIMIT {} OFFSET {}''',
        'QRY_FIND_BY_FILTERS': '''SELECT 
            car_code AS carCode, nm_proprietarios, cpf_cnpj_proprietarios,
            nm_imovel, alertcode, CAST(alertinsertedat AS STRING) as alertinsertedat, areaha,
            coordinates, CAST(detectedat AS STRING) as detectedat, geometry, id, source,
            statusid, car_id, CAST(statusinsertedat AS STRING) as statusinsertedat
            FROM private.mapbiomas_alerta {}
            ORDER BY detectedat DESC, areaha DESC
            LIMIT {} OFFSET {}''',
        'QRY_FIND_ALL': '''SELECT DISTINCT
            car_code AS carCode, nm_proprietarios, cpf_cnpj_proprietarios,
            nm_imovel, alertcode, CAST(alertinsertedat AS STRING) as alertinsertedat, areaha,
            coordinates, CAST(detectedat AS STRING) as detectedat, geometry, id, source,
            statusid, car_id, CAST(statusinsertedat AS STRING) as statusinsertedat
            FROM private.mapbiomas_alerta
            ORDER BY detectedat DESC, areaha DESC
            LIMIT {} OFFSET {}''',

        'QRY_COUNT_FIND_BY_CODE': '''SELECT COUNT(*) AS total_count
            FROM private.mapbiomas_alerta WHERE car_code = "{}"''',
        'QRY_COUNT_FIND_BY_CODES': '''SELECT COUNT(*) AS total_count 
            FROM private.mapbiomas_alerta WHERE car_code IN ({})''',
        'QRY_COUNT_FIND_BY_FILTERS': '''SELECT COUNT(*) AS total_count
            FROM private.mapbiomas_alerta {}''',
        'QRY_COUNT_FIND_ALL': '''SELECT COUNT(*) AS total_count
            FROM private.mapbiomas_alerta''',

        'QRY_OPTIONS_UF': '''SELECT DISTINCT(SUBSTR(car_code, 1, 2)) AS uf
            FROM private.mapbiomas_alerta''',
        'QRY_OPTIONS_RANGES': '''SELECT MIN(CAST(areaha AS DECIMAL)) AS min_areaha,
            MAX(CAST(areaha AS DECIMAL)) AS max_areaha, CAST(MIN(detectedat) AS STRING) AS min_detectedat,
            CAST(MAX(detectedat) AS STRING) AS max_detectedat
            FROM private.mapbiomas_alerta'''
    }

    def find_by_id(self, car, page):
        """ Localiza um município pelo código do IBGE """
        offset = (page - 1) * self.PAGE_SIZE
        query_dataset = self.get_named_query('QRY_FIND_BY_CODE').format(car, self.PAGE_SIZE, offset)
        dataset = pd.read_sql(query_dataset, self.get_dao()).to_dict(orient="records")

        if page == 1:
            query_count = self.get_named_query('QRY_COUNT_FIND_BY_CODE').format(car)
            count = pd.read_sql(query_count, self.get_dao()).to_dict(orient="records")

        return {"dataset": dataset, "metadata": count}

    def find_all(self, page):
        """ Localiza um município pelo código do IBGE """
        offset = (page - 1) * self.PAGE_SIZE
        query_dataset = self.get_named_query('QRY_FIND_ALL').format(self.PAGE_SIZE, offset)
        dataset = pd.read_sql(query_dataset, self.get_dao()).to_dict(orient="records")

        if page == 1:
            query_count = self.get_named_query('QRY_COUNT_FIND_ALL')
            count = pd.read_sql(query_count, self.get_dao()).to_dict(orient="records")[0]
            filter_options = self.find_filters_options()
            return {
                "dataset": dataset,
                "metadata": {**count, **filter_options}
            }
        return {"dataset": dataset}

    def find_by_id_list(self, car_list, page):
        """ Localiza um município pelo código do IBGE """
        offset = (page - 1) * self.PAGE_SIZE
        qry_param = ('\", \"').join(car_list)
        query_dataset = self.get_named_query('QRY_FIND_BY_CODES').format(f'\"{qry_param}"', self.PAGE_SIZE, offset)
        dataset = pd.read_sql(query_dataset, self.get_dao()).to_dict(orient="records")

        if page == 1:
            query_count = self.get_named_query('QRY_COUNT_FIND_BY_CODES')
            count = pd.read_sql(query_count, self.get_dao()).to_dict(orient="records")

        return {"dataset": dataset, "metadata": count}

    def find_by_filters(self, options, page):
        """ Finds a collection of CAR according to filters """
        offset = (page - 1) * self.PAGE_SIZE
        list_filters = []
        if 'cpfcnpj' in options and options.get('cpfcnpj') != ['undefined']:  # Filter by cpf/cnpj
            list_filters.append(f"cpf_cnpj_proprietarios LIKE '%{''.join(options.get('cpfcnpj'))}%'")
        if 'nome_proprietario' in options:  # Filter by name (partial)
            list_filters.append(f"nm_proprietarios LIKE '%{''.join(options.get('nome'))}%'")
        if 'siglauf' in options:  # Filter by name (partial)
            list_filters.append(f"estado = '{''.join(options.get('siglauf'))}'")
        # if 'nomemunicipio' in options:  # Filter by name (partial)
        #     list_filters.append(f"municipio LIKE '%{''.join(options.get('nomemunicipio'))}%'")
        if 'nome_propriedade' in options:
            list_filters.append(f"nm_propriedade LIKE '%{''.join(options.get('nome'))}%'")
        if 'arearange' in options:
            arearange = [float(x) for x in options.get("arearange").split(",")]
            list_filters.append(f"areaha BETWEEN {arearange[0]} AND {arearange[1]}")
        if 'daterange' in options:
            daterange = [datetime.strptime(x, "YYYY-MM-DD") for x in options.get("daterange").split(",")]
            list_filters.append(f"areaha BETWEEN {daterange[0]} AND {daterange[1]}")

        if len(list_filters) == 0:
            return None

        query_dataset = self.get_named_query('QRY_FIND_BY_FILTERS').format(
            f" WHERE {' AND '.join(list_filters)}",
            self.PAGE_SIZE,
            offset
        )
        dataset = pd.read_sql(query_dataset, self.get_dao()).to_dict(orient="records")

        if page == 1:
            query_count = self.get_named_query('QRY_COUNT_FIND_BY_FILTERS')
            count = pd.read_sql(query_count, self.get_dao()).to_dict(orient="records")

        return {"dataset": dataset, "metadata": count}

    def find_filters_options(self):
        result = pd.read_sql(self.get_named_query("QRY_OPTIONS_RANGES"), self.get_dao()).to_dict(orient="records")[0]
        result["uf"] = sorted(pd.read_sql(self.get_named_query("QRY_OPTIONS_UF"), self.get_dao())["uf"].tolist())
        return result


class MapBiomasConnectorRepository(RedisRepository):
    """ Repository to manage MapBiomas token"""
    KEY = "sue:er:mb:token"

    def __init__(self):
        self.load_and_prepare()

    def get_token(self):
        """ Get token from REDIS """
        return self.get_dao().get(self.KEY)

    def store_status(self, value):
        """Save token to REDIS """
        self.get_dao().set(self.KEY, value)