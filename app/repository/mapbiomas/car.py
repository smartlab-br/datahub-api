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
            FROM private.tb_cadastro_atividade_rural WHERE nu_recibo = "{}"'''
    }

    def find_by_id(self, car):
        """ Localiza um município pelo código do IBGE """
        query = self.get_named_query('QRY_FIND_BY_CODE').format(car)
        return pd.read_sql(query, self.get_dao()).to_dict(orient="records")
