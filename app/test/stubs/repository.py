""" Stubs for model testing """
import pandas as pd
from repository.base import BaseRepository, HadoopRepository
from repository.thematic import ThematicRepository

class StubRepository(BaseRepository):
    """ Fake repo to test instance methods """
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

    def __init__(self):
        """ Overrides constructor to avoid application context """
        self.dao = self.load_and_prepare()

    def load_and_prepare(self):
        """ Overriding method outside test scope """
        self.dao = 'Instanciei o DAO'


class StubNoLoadRepository(BaseRepository):
    """ Fake repo to test instance methods """
    def __init__(self):
        """ Overrides constructor to avoid application context """
        self.dao = self.load_and_prepare()


class StubHadoopRepository(HadoopRepository):
    """ Classe de STUB da abstração de repositórios hadoop (hive e impala) """
    VAL_FIELD = 'cd_indicador'
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
    DEFAULT_GROUPING = 'nu_competencia, cd_indicador'
    DEFAULT_PARTITIONING = 'cd_indicador'
    CNPJ_RAIZ_COLUMNS = {
        "rais": "nu_cnpj_raiz",
        "rfb": "nu_cnpj_raiz",
    }
    CNPJ_COLUMNS = {
        'rais': 'nu_cnpj_cei',
        'rfb': 'nu_cnpj',
    }
    COMPET_COLUMNS = {
        'rais': 'nu_ano_rais',
    }
    PF_COLUMNS = {
        'rais': 'nu_cpf',
        'rfb': 'nu_cpf_responsavel',
    }

    def __init__(self):
        """ Overrides constructor to avoid application context """

    def load_and_prepare(self):
        """ Overriding method outside test scope """
        self.dao = 'Instanciei o DAO'

    def fetch_data(self, query):
        """ Overriding methd outside test scope """
        return query


class StubNoLoadHadoopRepository(HadoopRepository):
    """ Classe de STUB da abstração de repositórios hadoop (hive e impala) """
    def __init__(self):
        """ Overrides constructor to avoid application context """
        self.dao = self.load_and_prepare()

    def fetch_data(self, query):
        """ Overriding methd outside test scope """
        return query


class StubFindModelRepository(StubHadoopRepository):
    """ Fake repo to test instance methods """

    def find_joined_dataset(self, options=None):
        """ Overriding method outside test scope """
        return self.find_dataset(options)

    #pylint: disable=R0201
    def find_dataset(self, _options=None):
        """ Retorno estático para execução dos testes """
        return pd.DataFrame([
            {"nm_indicador": "Ficticio", "nu_competencia": 2099, "vl_indicador": 1},
            {"nm_indicador": "Ficticio", "nu_competencia": 2047, "vl_indicador": 0.5}
        ])


class StubFindModelCutRepository(StubFindModelRepository):
    """ Fake repo to test instance methods """
    #pylint: disable=R0201
    def find_dataset(self, _options):
        """ Retorno estático para execução dos testes """
        return pd.DataFrame([
            {"idade": 10, "agr_count": 25},
            {"idade": 15, "agr_count": 25},
            {"idade": 20, "agr_count": 35},
            {"idade": 25, "agr_count": 50},
            {"idade": 30, "agr_count": 100},
            {"idade": 35, "agr_count": 43},
            {"idade": 60, "agr_count": 12}
        ])


class StubFindModelAgrRepository(StubFindModelRepository):
    """ Fake repo to test instance methods """
    def find_dataset(self, _options):
        """ Retorno estático para execução dos testes """
        return pd.DataFrame([
            {"nm_indicador": "Ficticio", "nu_competencia": 2099, "agr_sum_vl_indicador": 1},
            {"nm_indicador": "Ficticio", "nu_competencia": 2047, "agr_sum_vl_indicador": 0.5}
        ])


class StubThematicRepository(ThematicRepository):
    """ Fake repo to test instance methods """
    DEFAULT_GROUPING = 'nu_competencia, cd_indicador'
    DEFAULT_PARTITIONING = {
        'MAIN': 'cd_indicador',
        'NONE': [
            'municipio', 'assistenciasocial', 'sisben', 'catweb',
            'censoagronacional', 'censoagroestadual', 'censoagromunicipal',
            'coviddenunciampt', 'coviddocumentompt', 'coviddestinacaompt'
        ],
        'provabrasil': 'cd_tr_fora'
    }
    CNPJ_RAIZ_COLUMNS = {
        "rais": "nu_cnpj_raiz",
        "rfb": "nu_cnpj_raiz",
    }
    CNPJ_COLUMNS = {
        'rais': 'nu_cnpj_cei',
        'rfb': 'nu_cnpj',
    }
    COMPET_COLUMNS = {
        'rais': 'nu_ano_rais',
    }
    PF_COLUMNS = {
        'rais': 'nu_cpf',
        'rfb': 'nu_cpf_responsavel',
    }
    PERSP_VALUES = {
        'catweb': {
            'empregador': 'Empregador',
            'tomador': 'Tomador',
            'concessao': 'Empregador Concessão'
        }
    }

    def __init__(self):
        """ Overrides constructor to avoid application context """

    def load_and_prepare(self):
        """ Overriding method outside test scope """
        self.dao = 'Instanciei o DAO'
