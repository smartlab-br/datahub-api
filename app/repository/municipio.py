''' Repository para recuperar informações da CEE '''
from repository.base import ImpalaRepository
import pandas as pd

#pylint: disable=R0903
class MunicipioRepository(ImpalaRepository):
    ''' Definição do repo '''
    TABLE_NAMES = {
        'MAIN': 'municipio'
    }
    NAMED_QUERIES = {
        'QRY_FIND_DATASET': 'SELECT {} FROM {} {} {} {} {} {}',
        'QRY_FIND_BY_CODE': '''SELECT cd_municipio_ibge,cd_municipio_ibge_dv,st_situacao,cd_municipio_sinpas,cd_municipio_siafi,nm_municipio,nm_municipio_sem_acento,
                                      ds_observacao,cd_municipio_sinonimos,cd_municipio_sinonimos_dv,st_amazonia,st_fronteira,st_capital,cd_uf,ano_instalacao,
                                      ano_extincao,cd_municipio_sucessor,latitude,longitude,altitude,area,nm_uf,sg_uf,nm_municipio_uf,cd_unidade,cd_prt,nm_prt,
                                      nm_unidade,tp_unidade,sg_unidade,cd_mesorregiao,nm_mesorregiao,cd_microrregiao,nm_microrregiao,nu_portaria_mpt,tp_area,
                                      cd_geomunicipio_ibge,cd_municipio_rfb,cd_regiao,nm_regiao 
                               FROM municipio WHERE cd_municipio_ibge_dv = {}'''
    }

    def find_by_cd_ibge(self, cd_municipio_ibge):
        ''' Localiza um município pelo código do IBGE '''
        query = self.get_named_query('QRY_FIND_BY_CODE').format(cd_municipio_ibge)

        return pd.read_sql(query, self.get_dao())
