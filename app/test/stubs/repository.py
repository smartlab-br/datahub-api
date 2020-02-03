''' Stubs for model testing '''
from io import StringIO
import pandas as pd
from repository.base import BaseRepository, HadoopRepository

class StubRepository(BaseRepository):
    ''' Fake repo to test instance methods '''
    TABLE_NAMES = {
        'MAIN': 'indicadores',
        'municipio': 'municipio'
    }
    JOIN_SUFFIXES = {
        'municipio': '_mun'
    }
    ON_JOIN = {
        'municipio': 'cd_mun_ibge = cd_municipio_ibge_dv'
    }
    NAMED_QUERIES = {
        'QRY_FIND_DATASET': 'SELECT {} FROM {} {} {} {}',
        'QRY_FIND_JOINED_DATASET': 'SELECT {} FROM {} LEFT JOIN {} ON {} {} {} {}'
    }

    def load_and_prepare(self):
        ''' Overriding method outside test scope '''
        self.dao = 'Instanciei o DAO'

class StubHadoopRepository(HadoopRepository):
    ''' Classe de STUB da abstração de repositórios hadoop (hive e impala) '''
    TABLE_NAMES = {
        'MAIN': 'indicadores',
        'municipio': 'municipio'
    }
    JOIN_SUFFIXES = {
        'municipio': '_mun'
    }
    ON_JOIN = {
        'municipio': 'cd_mun_ibge = cd_municipio_ibge_dv'
    }
    NAMED_QUERIES = {
        'QRY_FIND_DATASET': 'SELECT {} FROM {} {} {} {} {} {}',
        'QRY_FIND_JOINED_DATASET': 'SELECT {} FROM {} LEFT JOIN {} ON {} {} {} {}'
    }
    def load_and_prepare(self):
        ''' Overriding method outside test scope '''
        self.dao = 'Instanciei o DAO'
    def fetch_data(self, query):
        ''' Overriding methd outside test scope '''
        return query

class StubFindModelRepository(StubRepository):
    ''' Fake repo to test instance methods '''
    def find_joined_dataset(self, options=None):
        ''' Overriding method outside test scope '''
        return self.find_dataset(options)

    #pylint: disable=R0201
    def find_dataset(self, _options):
        ''' Retorno estático para execução dos testes '''
        str_dataset = StringIO(
            """nm_indicador;nu_competencia;vl_indicador
                Ficticio;2099;1
                Ficticio;2047;0.5
                """
        )
        dataset = pd.read_csv(str_dataset, sep=";")
        return dataset

class StubFindModelAgrRepository(StubFindModelRepository):
    ''' Fake repo to test instance methods '''
    def find_dataset(self, _options):
        ''' Retorno estático para execução dos testes '''
        str_dataset = StringIO(
            """nm_indicador;nu_competencia;agr_sum_vl_indicador
                Ficticio;2099;1
                Ficticio;2047;0.5
                """
        )
        dataset = pd.read_csv(str_dataset, sep=";")
        return dataset
