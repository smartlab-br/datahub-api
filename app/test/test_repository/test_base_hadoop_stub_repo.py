'''Main tests in API'''
import unittest
from repository.base import HadoopRepository

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

class HadoopRepositoryFindDatasetTest(unittest.TestCase):
    ''' Classe que testa a obtenção de dados de tabela única '''
    def test_no_cats(self):
        ''' Lança exceção se não houver categoria nos parâmetros '''
        repo = StubHadoopRepository()
        options = {
            "valor": ['vl_indicador'],
            "agregacao": ['sum'],
            "ordenacao": ['-vl_indicador'],
            "where": ['eq-nu_competencia-2010']
        }
        self.assertRaises(
            KeyError,
            repo.find_dataset,
            options
        )

    def test_empty_cats(self):
        ''' Lança exceção se houver categorias vazias '''
        repo = StubHadoopRepository()
        options = {
            "categorias": [],
            "valor": ['vl_indicador'],
            "agregacao": ['sum'],
            "ordenacao": ['-vl_indicador'],
            "where": ['eq-nu_competencia-2010'],
            "pivot": None
        }
        self.assertRaises(
            ValueError,
            repo.find_dataset,
            options
        )

    def test_sql_injection_rejection(self):
        ''' Lança exceção se houver categorias com palavra bloqueada '''
        repo = StubHadoopRepository()
        options = {
            "categorias": ['nm_indicador;select', 'nu_competencia', 'vl_indicador'],
            "valor": ['vl_indicador'],
            "agregacao": ['sum'],
            "ordenacao": ['-vl_indicador'],
            "where": ['eq-nu_competencia-2010']
        }
        self.assertRaises(
            ValueError,
            repo.find_dataset,
            options
        )

    def test_full_query(self):
        ''' Verifica correta formação da query '''
        repo = StubHadoopRepository()
        options = {
            "categorias": ['nm_indicador', 'nu_competencia', 'vl_indicador'],
            "valor": ['vl_indicador'],
            "agregacao": ['sum'],
            "ordenacao": ['-nm_indicador'],
            "where": ['eq-nu_competencia-2010'],
            "pivot": None,
            "limit": None,
            "offset": None,
            "calcs": None
        }
        result = repo.find_dataset(options)
        self.assertEqual(
            result,
            ('SELECT  nm_indicador, nu_competencia, vl_indicador, '
             'sum(vl_indicador) AS agr_sum_vl_indicador FROM indicadores  '
             'WHERE nu_competencia = 2010 GROUP BY nm_indicador, '
             'nu_competencia, vl_indicador ORDER BY nm_indicador DESC  ')
        )

class HadoopRepositoryFindJoinedDatasetTest(unittest.TestCase):
    ''' Classe que testa a obtenção de dados de tabela com único join '''
    def test_no_cats(self):
        ''' Lança exceção se não houver categoria nos parâmetros '''
        repo = StubHadoopRepository()
        options = {
            "valor": ['vl_indicador'],
            "agregacao": ['sum'],
            "ordenacao": ['-vl_indicador'],
            "where": ['eq-nu_competencia-2010'],
            "joined": 'municipio'
        }
        self.assertRaises(
            KeyError,
            repo.find_joined_dataset,
            options
        )

    def test_empty_cats(self):
        ''' Lança exceção se houver categorias vazias '''
        repo = StubHadoopRepository()
        options = {
            "categorias": [],
            "valor": ['vl_indicador'],
            "agregacao": ['sum'],
            "ordenacao": ['-vl_indicador'],
            "where": ['eq-nu_competencia-2010'],
            "joined": 'municipio'
        }
        self.assertRaises(
            ValueError,
            repo.find_joined_dataset,
            options
        )

    def test_sql_injection_rejection(self):
        ''' Lança exceção se houver categorias com palavra bloqueada '''
        repo = StubHadoopRepository()
        options = {
            "categorias": ['nm_indicador;select', 'nu_competencia', 'vl_indicador'],
            "valor": ['vl_indicador'],
            "agregacao": ['sum'],
            "ordenacao": ['-vl_indicador'],
            "where": ['eq-nu_competencia-2010'],
            "joined": 'municipio'
        }
        self.assertRaises(
            ValueError,
            repo.find_dataset,
            options
        )

    def test_no_join(self):
        ''' Lança exceção se não houver join nos parâmetros '''
        repo = StubHadoopRepository()
        options = {
            "categorias": ['nm_indicador', 'nu_competencia', 'vl_indicador'],
            "valor": ['vl_indicador'],
            "agregacao": ['sum'],
            "ordenacao": ['-vl_indicador'],
            "where": ['eq-nu_competencia-2010']
        }
        self.assertRaises(
            KeyError,
            repo.find_joined_dataset,
            options
        )

    def test_full_query_limit_offset(self):
        ''' Verifica correta formação da query com limit e offset'''
        repo = StubHadoopRepository()
        options = {
            "categorias": ['nm_indicador', 'nu_competencia', 'vl_indicador', 'lat', 'long'],
            "valor": ['vl_indicador'],
            "agregacao": ['sum'],
            "ordenacao": ['-nm_indicador'],
            "where": ['eq-nu_competencia-2010'],
            "pivot": None,
            "limit": '1',
            "offset": '5',
            "calcs": None
        }
        result = repo.find_dataset(options)
        expected = ('SELECT  nm_indicador, nu_competencia, vl_indicador, '
                    'lat, long, sum(vl_indicador) AS agr_sum_vl_indicador '
                    'FROM indicadores  WHERE nu_competencia = 2010 GROUP BY '
                    'nm_indicador, nu_competencia, vl_indicador, lat, long '
                    'ORDER BY nm_indicador DESC LIMIT 1 OFFSET 5')
        self.assertEqual(result, expected)
