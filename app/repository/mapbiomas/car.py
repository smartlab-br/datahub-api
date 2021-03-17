''' Repository para recuperar informações da CEE '''
import pandas as pd
from repository.base import ImpalaRepository

#pylint: disable=R0903
class CarRepository(ImpalaRepository):
    ''' Definição do repo '''
    TABLE_NAMES = {
        'MAIN': 'car'
    }
    NAMED_QUERIES = {
        'QRY_FIND_DATASET': 'SELECT {} FROM {} {} {} {} {} {}',
        'QRY_FIND_BY_CODE': '''SELECT 
            nu_recibo AS carCode, nm_proprietarios, cpf_cnpj_proprietarios 
            FROM private.tb_cadastro_atividade_rural WHERE nu_recibo = "{}"''',
        'QRY_FIND_BY_FILTERS': '''SELECT 
            nu_recibo AS carCode, nm_proprietarios, cpf_cnpj_proprietarios 
            FROM private.tb_cadastro_atividade_rural {}'''
    }

    def find_by_id(self, car):
        """ Localiza um município pelo código do IBGE """
        query = self.get_named_query('QRY_FIND_BY_CODE').format(car)
        return pd.read_sql(query, self.get_dao()).to_dict(orient="records")

    def find_by_filters(self, options):
        """ Finds a collection of CAR according to filters """
        list_filters = []
        if 'cpfcnpj' in options:  # Filter by cpf/cnpj
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