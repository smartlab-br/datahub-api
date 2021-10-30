''' Repository para recuperar informações da CEE '''
import pandas as pd
from repository.base import ImpalaRepository, RedisRepository

#pylint: disable=R0903
class CarRepository(ImpalaRepository):
    ''' Definição do repo '''
    TABLE_NAMES = {
        'MAIN': 'car'
    }
    NAMED_QUERIES = {
        'QRY_FIND_DATASET': 'SELECT {} FROM {} {} {} {} {} {}',
        'QRY_FIND_BY_CODE': '''SELECT 
            car_code AS carCode, nm_proprietarios, cpf_cnpj_proprietarios,
            nm_imovel, alertcode, CAST(alertinsertedat AS STRING) as alertinsertedat, areaha,
            coordinates, CAST(detectedat AS STRING) as detectedat, geometry, id, source,
            statusid, car_id, CAST(statusinsertedat AS STRING) as statusinsertedat
            FROM private.mapbiomas_alerta WHERE car_code = "{}" LIMIT 50''',
        'QRY_FIND_BY_CODES': '''SELECT 
            car_code AS carCode, nm_proprietarios, cpf_cnpj_proprietarios,
            nm_imovel, alertcode, CAST(alertinsertedat AS STRING) as alertinsertedat, areaha,
            coordinates, CAST(detectedat AS STRING) as detectedat, geometry, id, source,
            statusid, car_id, CAST(statusinsertedat AS STRING) statusinsertedat
            FROM private.mapbiomas_alerta WHERE car_code IN ({}) LIMIT 50''',
        'QRY_FIND_BY_FILTERS': '''SELECT 
            car_code AS carCode, nm_proprietarios, cpf_cnpj_proprietarios,
            nm_imovel, alertcode, CAST(alertinsertedat AS STRING) as alertinsertedat, areaha,
            coordinates, CAST(detectedat AS STRING) as detectedat, geometry, id, source,
            statusid, car_id, CAST(statusinsertedat AS STRING) as statusinsertedat
            FROM private.mapbiomas_alerta {} LIMIT 50''',
        'QRY_FIND_ALL': '''SELECT DISTINCT
            car_code AS carCode, nm_proprietarios, cpf_cnpj_proprietarios,
            nm_imovel, alertcode, CAST(alertinsertedat AS STRING) as alertinsertedat, areaha,
            coordinates, CAST(detectedat AS STRING) as detectedat, geometry, id, source,
            statusid, car_id, CAST(statusinsertedat AS STRING) as statusinsertedat
            FROM private.mapbiomas_alerta LIMIT 50'''
    }

    def find_by_id(self, car):
        """ Localiza um município pelo código do IBGE """
        query = self.get_named_query('QRY_FIND_BY_CODE').format(car)
        return pd.read_sql(query, self.get_dao()).to_dict(orient="records")

    def find_all(self, car):
        """ Localiza um município pelo código do IBGE """
        query = self.get_named_query('QRY_FIND_ALL').format(car)
        return pd.read_sql(query, self.get_dao()).to_dict(orient="records")

    def find_by_id_list(self, car_list):
        """ Localiza um município pelo código do IBGE """
        qry_param = ('\", \"').join(car_list)
        query = self.get_named_query('QRY_FIND_BY_CODES').format(f'\"{qry_param}"')
        return pd.read_sql(query, self.get_dao()).to_dict(orient="records")

    def find_by_filters(self, options):
        """ Finds a collection of CAR according to filters """
        list_filters = []
        if 'cpfcnpj' in options and options.get('cpfcnpj') != ['undefined']:  # Filter by cpf/cnpj
            list_filters.append(f"cpf_cnpj_proprietarios LIKE '%{''.join(options.get('cpfcnpj'))}%'")
        if 'nome' in options:  # Filter by name (partial)
            list_filters.append(f"nm_proprietarios LIKE '%{''.join(options.get('nome'))}%'")
        if 'siglauf' in options:  # Filter by name (partial)
            list_filters.append(f"estado = '{''.join(options.get('siglauf'))}'")
        if 'nomemunicipio' in options:  # Filter by name (partial)
            list_filters.append(f"municipio LIKE '%{''.join(options.get('nomemunicipio'))}%'")

        if len(list_filters) == 0:
            return None

        query = self.get_named_query('QRY_FIND_BY_FILTERS').format(f" WHERE {' AND '.join(list_filters)}")

        return pd.read_sql(query, self.get_dao()).to_dict(orient="records")


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