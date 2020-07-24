'''Main tests in API'''
import unittest
from test.stubs.repository import StubHadoopRepository

class StubHadoopRepositoryCustomPartition(StubHadoopRepository):
    ''' Fake repo to test instance methods '''
    DEFAULT_PARTITIONING = ''

class StubHadoopRepositoryCustomPartitionMultipleValues(StubHadoopRepository):
    ''' Fake repo to test instance methods '''
    DEFAULT_PARTITIONING = 'a, b, c'

class BaseHadoopRepositoryGeneralTest(unittest.TestCase):
    ''' General tests over StubRepo '''
    def test_get_partitioning_empty(self):
        ''' Verifica correta obtenção de cláusula de partitioning quando não há
            particionamento especificado na classe '''
        repo = StubHadoopRepositoryCustomPartition()
        self.assertEqual(
            repo.replace_partition("min_part"),
            'MIN({val_field}) OVER() AS api_calc_{calc}'
        )

    def test_exclude_from_partition(self):
        ''' Verifica a correta exclusão do particionamento de campos inexistentes no SELECT '''
        repo = StubHadoopRepositoryCustomPartitionMultipleValues()
        self.assertEqual(repo.exclude_from_partition(['a'], ['count']), 'a')

    def test_get_partitioning_default(self):
        ''' Verifica correta obtenção dde cláusula de particionamento '''
        repo = StubHadoopRepository()
        self.assertEqual(
            repo.replace_partition("min_part"),
            'MIN({val_field}) OVER(PARTITION BY {partition}) AS api_calc_{calc}'
        )

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

class BaseHadoopRepositoryNamedQueryTest(unittest.TestCase):
    ''' Validates recovery of named query '''
    def test_validate_positive(self):
        ''' Verifica correta obtenção de named query '''
        repo = StubHadoopRepository()
        qry_name = repo.get_named_query('QRY_FIND_DATASET')
        self.assertEqual(qry_name, 'SELECT {} FROM {} {} {} {} {} {}')

    def test_validate_negative(self):
        ''' Verifica comportamento de obtenção de named query não mapeada '''
        repo = StubHadoopRepository()
        self.assertRaises(KeyError, repo.get_named_query, 'FAKE_QUERY')

class BaseRepositoryJoinSuffixTest(unittest.TestCase):
    ''' Validates recovery of join suffix '''
    def test_validate_positive(self):
        ''' Verifica correta obtenção de sufixo '''
        repo = StubHadoopRepository()
        sfx_name = repo.get_join_suffix('municipio')
        self.assertEqual(sfx_name, '_mun')

    def test_validate_negative(self):
        ''' Verifica comportamento de obtenção de sufixo não mapeado '''
        repo = StubHadoopRepository()
        self.assertRaises(KeyError, repo.get_join_suffix, 'galaxia')

class BaseHadoopRepositoryStdCalcsTest(unittest.TestCase):
    ''' Classe de teste de geração de string para cálculos com partitioning '''
    def test_std_calc_max(self):
        ''' Testa um cálculo de min e max '''
        options = {
            "valor": "vl_indicador",
            "calcs": ["min_part", "max_part"],
            "categorias": ["cd_mun_ibge", "nu_ano"]
        }
        repo = StubHadoopRepository()
        self.assertEqual(
            repo.build_std_calcs(options),
            ('MIN(vl_indicador) OVER(PARTITION BY cd_indicador) AS api_calc_min_part, '
             'MAX(vl_indicador) OVER(PARTITION BY cd_indicador) AS api_calc_max_part'
            )
        )

    def test_std_calc_avg(self):
        ''' Testa um cálculo de soma, que deve gerar, adicionalmente, min e max '''
        options = {
            "valor": "vl_indicador",
            "calcs": ["avg_part"],
            "categorias": ["cd_mun_ibge", "nu_ano"]
        }
        repo = StubHadoopRepository()
        self.assertEqual(
            repo.build_std_calcs(options),
            ('MIN(vl_indicador) OVER(PARTITION BY cd_indicador) AS api_calc_min_part, '
             'MAX(vl_indicador) OVER(PARTITION BY cd_indicador) AS api_calc_max_part, '
             'AVG(vl_indicador) OVER(PARTITION BY cd_indicador) AS api_calc_avg_part'
            )
        )

    def test_std_calc_default_partitioning_empty_string(self):
        ''' Testa um cálculo com partitioning padrão vazia '''
        options = {
            "valor": "vl_indicador",
            "calcs": ["min_part", "max_part"],
            "categorias": ["cd_mun_ibge", "nu_ano"]
        }
        repo = StubHadoopRepositoryCustomPartition()
        self.assertEqual(
            repo.build_std_calcs(options),
            ('MIN(vl_indicador) OVER() AS api_calc_min_part, '
             'MAX(vl_indicador) OVER() AS api_calc_max_part'
            )
        )

    def test_std_calc_default_partitioning(self):
        ''' Testa um cálculo com partitioning padrão existente '''
        options = {
            "valor": "vl_indicador",
            "calcs": ["min_part", "max_part"],
            "categorias": ["cd_mun_ibge", "nu_ano"]
        }
        repo = StubHadoopRepositoryCustomPartitionMultipleValues()
        self.assertEqual(
            repo.build_std_calcs(options),
            ('MIN(vl_indicador) OVER(PARTITION BY a, b, c) AS api_calc_min_part, '
             'MAX(vl_indicador) OVER(PARTITION BY a, b, c) AS api_calc_max_part'
            )
        )

    def test_std_calc_custom_partitioning(self):
        ''' Testa um cálculo com sobrescrita do partitioning '''
        options = {
            "valor": "vl_indicador",
            "calcs": ["min_part", "max_part"],
            "categorias": ["cd_mun_ibge", "nu_ano"],
            "partition": "nu_ano"
        }
        repo = StubHadoopRepository()
        self.assertEqual(
            repo.build_std_calcs(options),
            ('MIN(vl_indicador) OVER(PARTITION BY nu_ano) AS api_calc_min_part, '
             'MAX(vl_indicador) OVER(PARTITION BY nu_ano) AS api_calc_max_part'
            )
        )

    def test_std_calc_invalid_calc(self):
        ''' Testa se lança exceção quando envia um tipo de cálculo não previsto '''
        options = {
            "valor": "vl_indicador",
            "calcs": ["sum"],
            "categorias": ["cd_mun_ibge", "nu_ano"],
            "partition": "nu_ano"
        }
        repo = StubHadoopRepository()
        self.assertRaises(
            KeyError,
            repo.build_std_calcs,
            options
        )
class BaseRepositoryCombineValAggrTest(unittest.TestCase):
    ''' Classe de teste de combinações entre valor e agregação '''
    def test_one_val_one_aggr(self):
        ''' Um valor, uma agregação, sem sufixo. '''
        repo = StubHadoopRepository()
        valor = ['vl_indicador']
        agregacao = ['sum']
        result = repo.combine_val_aggr(valor, agregacao)
        self.assertEqual(result, ['sum(vl_indicador) AS agr_sum_vl_indicador'])

    def test_one_val_one_aggr_suffix(self):
        ''' Um valor, uma agregação, com sufixo. '''
        repo = StubHadoopRepository()
        valor = ['vl_indicador_mun']
        agregacao = ['sum']
        result = repo.combine_val_aggr(valor, agregacao, '_mun')
        self.assertEqual(result, ['sum(vl_indicador) AS agr_sum_vl_indicador'])

    def test_one_val_n_aggr(self):
        ''' Um valor, n agregações, sem sufixo. '''
        repo = StubHadoopRepository()
        valor = ['vl_indicador']
        agregacao = ['sum', 'count']
        result = repo.combine_val_aggr(valor, agregacao)
        self.assertEqual(
            result,
            ['sum(vl_indicador) AS agr_sum_vl_indicador',
             'count(vl_indicador) AS agr_count_vl_indicador']
        )

    def test_one_val_n_aggr_suffix(self):
        ''' Um valor, n agregações, com sufixo. '''
        repo = StubHadoopRepository()
        valor = ['vl_indicador_mun']
        agregacao = ['sum', 'count']
        result = repo.combine_val_aggr(valor, agregacao, '_mun')
        self.assertEqual(
            result,
            ['sum(vl_indicador) AS agr_sum_vl_indicador',
             'count(vl_indicador) AS agr_count_vl_indicador']
        )

    def test_n_val_one_aggr(self):
        ''' N valores, uma agregação, sem sufixo. '''
        repo = StubHadoopRepository()
        valor = ['nu_competencia', 'vl_indicador']
        agregacao = ['count']
        result = repo.combine_val_aggr(valor, agregacao)
        self.assertEqual(
            result,
            ('count(nu_competencia) AS agr_count_nu_competencia, '
             'count(vl_indicador) AS agr_count_vl_indicador')
        )

    def test_n_val_one_aggr_suffix(self):
        ''' N valores, uma agregação, com sufixo. '''
        repo = StubHadoopRepository()
        valor = ['nu_competencia_mun', 'vl_indicador_mun']
        agregacao = ['count']
        result = repo.combine_val_aggr(valor, agregacao, '_mun')
        self.assertEqual(
            result,
            ('count(nu_competencia) AS agr_count_nu_competencia, '
             'count(vl_indicador) AS agr_count_vl_indicador')
        )

    def test_n_val_n_aggr(self):
        ''' N valores, uma agregação, sem sufixo. '''
        repo = StubHadoopRepository()
        valor = ['nu_competencia', 'vl_indicador']
        agregacao = ['sum-count', 'sum-count']
        result = repo.combine_val_aggr(valor, agregacao)
        self.assertEqual(
            result,
            ('sum(nu_competencia) AS agr_sum_nu_competencia, '
             'count(nu_competencia) AS agr_count_nu_competencia, '
             'sum(vl_indicador) AS agr_sum_vl_indicador, count(vl_indicador) '
             'AS agr_count_vl_indicador')
        )

    def test_n_val_n_aggr_suffix(self):
        ''' N valores, n agregações, com sufixo. '''
        repo = StubHadoopRepository()
        valor = ['nu_competencia_mun', 'vl_indicador_mun']
        agregacao = ['sum-count', 'sum-count']
        result = repo.combine_val_aggr(valor, agregacao, '_mun')
        self.assertEqual(
            result,
            ('sum(nu_competencia) AS agr_sum_nu_competencia, '
             'count(nu_competencia) AS agr_count_nu_competencia, '
             'sum(vl_indicador) AS agr_sum_vl_indicador, count(vl_indicador) '
             'AS agr_count_vl_indicador')
        )

class BaseRepositoryBuildOrderStringTest(unittest.TestCase):
    ''' Classe que monta o array de valores ordenados '''
    def test_invalid(self):
        ''' Retorna exceção quando a ordenação é inválida '''
        ordenacao = ['nm_indicador;select', 'nu_competencia']
        repo = StubHadoopRepository()
        self.assertRaises(
            ValueError,
            repo.build_order_string,
            ordenacao
        )

    def test_null_agregation(self):
        ''' Retorna string vazia se não houver ordenação '''
        ordenacao = None
        repo = StubHadoopRepository()
        result = repo.build_order_string(ordenacao)
        self.assertEqual(result, '')

    def test_empty_agregation(self):
        ''' Retorna string vazia se houver ordenação vazia '''
        ordenacao = []
        repo = StubHadoopRepository()
        result = repo.build_order_string(ordenacao)
        self.assertEqual(result, '')

    def test_valid_agregation(self):
        ''' Verifica string de retorno em condição válida '''
        ordenacao = ['nm_indicador', 'nu_competencia', '-vl_indicador']
        repo = StubHadoopRepository()
        result = repo.build_order_string(ordenacao)
        expected = 'ORDER BY nm_indicador, nu_competencia, vl_indicador DESC'
        self.assertEqual(result, expected)

class BaseRepositoryBuildJoinedGroupStringTest(unittest.TestCase):
    ''' Classe de construção da cláusula do join '''
    def test_invalid_cats(self):
        ''' Lança erro ao tentar agrupar sem categoria. '''
        repo = StubHadoopRepository()
        cats = None
        agrs = None
        joined = 'municipio'
        self.assertRaises(
            ValueError,
            repo.build_joined_grouping_string,
            cats,
            agrs,
            joined
        )

    def test_invalid_join(self):
        ''' Lança erro ao tentar agrupar sem join. '''
        repo = StubHadoopRepository()
        cats = ['nm_indicador', 'vl_indicador']
        agrs = None
        joined = None
        self.assertRaises(
            KeyError,
            repo.build_joined_grouping_string,
            cats,
            agrs,
            joined
        )

    def test_default(self):
        ''' Check if suffix removal work in group by with join '''
        repo = StubHadoopRepository()
        cats = ['nm_indicador', 'lat_mun']
        agrs = ['nm_indicador']
        joined = 'municipio'
        result = repo.build_joined_grouping_string(cats, agrs, joined)
        self.assertEqual(result, 'GROUP BY nm_indicador, lat')

    def test_renamed_cat(self):
        ''' Check if rename is ignored when building grouping string '''
        repo = StubHadoopRepository()
        cats = ['nm_indicador', 'lat-latitude']
        agrs = ['nm_indicador']
        joined = 'municipio'
        result = repo.build_joined_grouping_string(cats, agrs, joined)
        self.assertEqual(result, 'GROUP BY nm_indicador, lat')

    def test_renamed_cat_joined(self):
        ''' Check if rename/suffix are ignored when building group string '''
        repo = StubHadoopRepository()
        cats = ['nm_indicador', 'lat_mun-latitude']
        agrs = ['nm_indicador']
        joined = 'municipio'
        result = repo.build_joined_grouping_string(cats, agrs, joined)
        self.assertEqual(result, 'GROUP BY nm_indicador, lat')

    def test_invalid_agregation(self):
        ''' Lança erro ao tentar agrupar sem join. '''
        repo = StubHadoopRepository()
        cats = ['nm_indicador', 'vl_indicador']
        agrs = None
        joined = 'municipio'
        self.assertRaises(
            ValueError,
            repo.build_joined_grouping_string,
            cats,
            agrs,
            joined
        )

    def test_with_distinct(self):
        ''' Check if string is empty when DISTINCT is used '''
        repo = StubHadoopRepository()
        cats = ['nm_indicador', 'lat_mun-latitude']
        agrs = ['distinct']
        joined = 'municipio'
        result = repo.build_joined_grouping_string(cats, agrs, joined)
        self.assertEqual(result, '')

class BaseRepositoryBuildJoinedCategoriasTest(unittest.TestCase):
    ''' Classe de construção das categorias '''
    def test_no_cats(self):
        ''' Lança exceção quando não há categorias. '''
        repo = StubHadoopRepository()
        cats = None
        valor = ['vl_indicador']
        agregacao = ['sum']
        joined = 'municipio'
        self.assertRaises(
            ValueError,
            repo.build_joined_categorias,
            cats,
            valor,
            agregacao,
            joined
        )

    def test_empty_cats(self):
        ''' Lança exceção quando há categorias vazias. '''
        repo = StubHadoopRepository()
        cats = []
        valor = ['vl_indicador']
        agregacao = ['sum']
        joined = 'municipio'
        self.assertRaises(
            ValueError,
            repo.build_joined_categorias,
            cats,
            valor,
            agregacao,
            joined
        )

    def test_no_valor(self):
        ''' Retorna normalmente quando não há valor. '''
        repo = StubHadoopRepository()
        cats = ['cd_indicador', 'nu_competencia', 'vl_indicador', 'lat_mun', 'long_mun']
        valor = None
        agregacao = ['sum']
        joined = 'municipio'
        result = repo.build_joined_categorias(cats, valor, agregacao, joined)
        self.assertEqual(
            result,
            ('cd_indicador, nu_competencia, vl_indicador, lat, long, sum(*) '
             'AS agr_sum')
        )

    def test_no_agrs(self):
        ''' Retorna normalmente quando não há agregações. '''
        repo = StubHadoopRepository()
        cats = ['cd_indicador', 'nu_competencia', 'vl_indicador', 'lat_mun', 'long_mun']
        valor = ['vl_indicador']
        agregacao = None
        joined = 'municipio'
        result = repo.build_joined_categorias(cats, valor, agregacao, joined)
        self.assertEqual(result, 'cd_indicador, nu_competencia, vl_indicador, lat, long')

    def test_no_join(self):
        ''' Retorna normalmente quando não há join. '''
        repo = StubHadoopRepository()
        cats = ['cd_indicador', 'nu_competencia', 'vl_indicador']
        valor = ['vl_indicador']
        agregacao = ['sum', 'pct_sum']
        joined = None
        self.assertRaises(
            KeyError,
            repo.build_joined_categorias,
            cats,
            valor,
            agregacao,
            joined
        )

    def test_full_join(self):
        ''' Retorna normalmente. '''
        repo = StubHadoopRepository()
        cats = ['cd_indicador', 'nu_competencia', 'vl_indicador', 'lat_mun', 'long_mun']
        valor = ['vl_indicador']
        agregacao = ['sum', 'pct_sum']
        joined = 'municipio'
        expected = ('cd_indicador, nu_competencia, vl_indicador, lat, long, '
                    'sum(vl_indicador) AS agr_sum_vl_indicador, '
                    'SUM(vl_indicador) * 100 / SUM(vl_indicador) OVER() AS '
                    'agr_pct_sum_vl_indicador')
        result = repo.build_joined_categorias(cats, valor, agregacao, joined)
        self.assertEqual(result, expected)

    def test_invalid(self):
        ''' Lança exceção quando um campo é inválido. '''
        repo = StubHadoopRepository()
        cats = ['cd_indicador;', 'nu_competencia', 'vl_indicador']
        valor = ['vl_indicador']
        agregacao = ['sum', 'pct_sum']
        joined = 'municipio'
        self.assertRaises(
            ValueError,
            repo.build_joined_categorias,
            cats,
            valor,
            agregacao,
            joined
        )

class BaseRepositoryBuildGenericAgrArrayTest(unittest.TestCase):
    ''' Classe que monta o array de valores agregados '''
    def test_invalid(self):
        ''' Retorna exceção quando a agregação é inválida '''
        agr = ['count', 'CSTM']
        repo = StubHadoopRepository()
        self.assertRaises(
            ValueError,
            repo.build_generic_agr_array,
            agr
        )

    def test_null_agregation(self):
        ''' Retorna string vazia se não houver agregação '''
        agr = None
        repo = StubHadoopRepository()
        result = repo.build_generic_agr_array(agr)
        self.assertEqual(result, [])

    def test_empty_agregation(self):
        ''' Retorna string vazia se não houver agregação '''
        agr = []
        repo = StubHadoopRepository()
        result = repo.build_generic_agr_array(agr)
        self.assertEqual(result, [])

    def test_valid_agregation(self):
        ''' Retorna string vazia se não houver agregação '''
        agr = ['count', 'sum', 'distinct']
        repo = StubHadoopRepository()
        result = repo.build_generic_agr_array(agr)
        expected = [
            'count(*) AS agr_count',
            'sum(*) AS agr_sum'
        ]
        self.assertEqual(result, expected)

class BaseRepositoryBuildFilterStringTest(unittest.TestCase):
    ''' Classe de construção da cláusula do join '''
    def test_no_where(self):
        ''' Retorna branco ao tentar filtrar sem where. '''
        repo = StubHadoopRepository()
        whrs = None
        is_on = False
        joined = None
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(result, '')

    def test_empty_where(self):
        ''' Retorna branco ao tentar filtrar com where vazio. '''
        repo = StubHadoopRepository()
        whrs = []
        is_on = False
        joined = None
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(result, '')

    def test_simple_valid(self):
        ''' Retorna cláusula where de consulta sem join. '''
        repo = StubHadoopRepository()
        whrs = ['eq-nu_competencia-2010', 'and', 'eq-cd_indicador-01_02_03_04']
        is_on = False
        joined = None
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(result, 'nu_competencia = 2010 and cd_indicador = 01_02_03_04')

    def test_hyphen_valid(self):
        ''' Retorna cláusula where de consulta sem join, com hífen. '''
        repo = StubHadoopRepository()
        whrs = ['eq-nu_competencia-2010', 'and', 'eq-cd_indicador-01\\-02\\-03\\-04']
        is_on = False
        joined = None
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(result, 'nu_competencia = 2010 and cd_indicador = 01-02-03-04')

    def test_in_clause(self):
        ''' Retorna cláusula where de consulta com cláusula IN. '''
        repo = StubHadoopRepository()
        whrs = ['eq-nu_competencia-2010', 'and',
                'in-cd_indicador-01_02_03_04-01_02_03_05-01_02_03_06']
        is_on = False
        joined = None
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(
            result,
            ('nu_competencia = 2010 and cd_indicador IN (01_02_03_04,'
             '01_02_03_05,01_02_03_06)')
        )

    def test_valid_where_join(self):
        ''' Retorna cláusula where de consulta com join. '''
        repo = StubHadoopRepository()
        whrs = ['eq-nu_competencia-2010', 'and', 'eq-cd_indicador-01_02_03_04']
        is_on = False
        joined = 'municipio'
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(result, 'nu_competencia = 2010 and cd_indicador = 01_02_03_04')

    def test_valid_empty_where_join(self):
        ''' Retorna cláusula where vazia de consulta com join. '''
        repo = StubHadoopRepository()
        whrs = ['gt-lat_mun-0', 'gt-long_mun-0']
        is_on = False
        joined = 'municipio'
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(result, '')

    def test_valid_empty_on_join(self):
        ''' Retorna cláusula on vazia de consulta com join. '''
        repo = StubHadoopRepository()
        whrs = ['eq-nu_competencia-2010', 'eq-cd_indicador-01_02_03_04']
        is_on = True
        joined = 'municipio'
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(result, '')

    def test_valid_on_join(self):
        ''' Retorna cláusula on de consulta com join. '''
        repo = StubHadoopRepository()
        whrs = ['gt-lat_mun-0', 'gt-long_mun-0']
        is_on = True
        joined = 'municipio'
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(result, 'lat_mun > 0 long_mun > 0')

    def test_invalid_on_join(self):
        ''' Retorna cláusula where de consulta com join. '''
        repo = StubHadoopRepository()
        whrs = ['gt-lat_mun-0', 'gt-long_mun-0']
        is_on = True
        joined = None
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(result, '')

class BaseRepositoryBuildCategoriasTest(unittest.TestCase):
    ''' Classe de construção das categorias '''
    def test_no_cats(self):
        ''' Lança exceção quando não há categorias. '''
        repo = StubHadoopRepository()
        cats = None
        options = {
            "categorias": cats,
            "valor": ['vl_indicador'],
            "agregacao": ['sum']
        }
        self.assertRaises(
            ValueError,
            repo.build_categorias,
            cats,
            options
        )

    def test_empty_cats(self):
        ''' Lança exceção quando há categorias vazias. '''
        repo = StubHadoopRepository()
        cats = []
        options = {
            "categorias": cats,
            "valor": ['vl_indicador'],
            "agregacao": ['sum']
        }
        self.assertRaises(
            ValueError,
            repo.build_categorias,
            cats,
            options
        )

    def test_no_valor(self):
        ''' Retorna normalmente quando não há valor. '''
        repo = StubHadoopRepository()
        cats = ['cd_indicador', 'nu_competencia', 'vl_indicador']
        options = {
            "categorias": cats,
            "valor": None,
            "agregacao": ['sum']
        }
        result = repo.build_categorias(cats, options)
        self.assertEqual(result, ' cd_indicador, nu_competencia, vl_indicador, sum(*) AS agr_sum')

    def test_no_agrs(self):
        ''' Retorna normalmente quando não há agregações. '''
        repo = StubHadoopRepository()
        cats = ['cd_indicador', 'nu_competencia', 'vl_indicador']
        options = {
            "categorias": cats,
            "valor": ['vl_indicador'],
            "agregacao": None
        }
        result = repo.build_categorias(cats, options)
        self.assertEqual(result, ' cd_indicador, nu_competencia, vl_indicador, vl_indicador')

    def test_full(self):
        ''' Retorna normalmente quando não há agregações. '''
        repo = StubHadoopRepository()
        cats = ['cd_indicador', 'nu_competencia', 'vl_indicador']
        options = {
            "categorias": cats,
            "valor": ['vl_indicador'],
            "agregacao": ['sum', 'pct_sum']
        }
        expected = (' cd_indicador, nu_competencia, vl_indicador, '
                    'sum(vl_indicador) AS agr_sum_vl_indicador, '
                    'SUM(vl_indicador) * 100 / SUM(vl_indicador) OVER() AS '
                    'agr_pct_sum_vl_indicador')
        result = repo.build_categorias(cats, options)
        self.assertEqual(result, expected)

    def test_invalid(self):
        ''' Lança exceção quando um campo é inválido. '''
        repo = StubHadoopRepository()
        cats = ['cd_indicador;', 'nu_competencia', 'vl_indicador']
        options = {
            "categorias": cats,
            "valor": ['vl_indicador'],
            "agregacao": ['sum', 'pct_sum']
        }
        self.assertRaises(
            ValueError,
            repo.build_categorias,
            cats,
            options
        )

class BaseRepositoryBuildAgrArrayTest(unittest.TestCase):
    ''' Classe que monta o array de valores agregados '''
    def test_invalid(self):
        ''' Retorna exceção quando a agregação é inválida '''
        vlr = 'vl_indicador'
        agr = ['sum', 'CSTM']
        repo = StubHadoopRepository()
        self.assertRaises(
            ValueError,
            repo.build_agr_array,
            vlr,
            agr
        )

    def test_null_agregation(self):
        ''' Retorna string vazia se não houver agregação '''
        vlr = 'vl_indicador'
        agr = None
        repo = StubHadoopRepository()
        result = repo.build_agr_array(vlr, agr)
        self.assertEqual(result, [])

    def test_empty_agregation(self):
        ''' Retorna string vazia se não houver agregação '''
        vlr = 'vl_indicador'
        agr = []
        repo = StubHadoopRepository()
        result = repo.build_agr_array(vlr, agr)
        self.assertEqual(result, [])

    def test_valid_agregation(self):
        ''' Retorna string vazia se não houver agregação '''
        vlr = 'vl_indicador'
        agr = ['sum', 'max', 'distinct']
        repo = StubHadoopRepository()
        result = repo.build_agr_array(vlr, agr)
        expected = [
            'sum(vl_indicador) AS agr_sum_vl_indicador',
            'max(vl_indicador) AS agr_max_vl_indicador'
        ]
        self.assertEqual(result, expected)

class HadoopRepositoryBuildFilterStringTest(unittest.TestCase):
    ''' Tests complex criteria string builder '''
    FILTER_LIST = [
        'nl-field', 'and', 'eq-field-value', 'and',
        'in-field-a-b', 'and', 'ltsz-column-value'
    ]
    EXPECTED = "field IS NULL and field = value and field IN (a,b) and LENGTH(CAST(column AS STRING)) < value"

    def test_complete_string(self):
        ''' Explores different possibilities in a single string building '''
        self.assertEqual(
            StubHadoopRepository().build_filter_string(
                self.FILTER_LIST
            ),
            self.EXPECTED
        )

    def test_complete_string_no_where(self):
        ''' Tests if empty string is returned when no filter list is received '''
        self.assertEqual(StubHadoopRepository().build_filter_string(None), '')

    def test_complete_string_is_on_no_join(self):
        ''' Tests if empty string is returned when the flag of ON filter is
            set, but no join info is given '''
        self.assertEqual(
            StubHadoopRepository().build_filter_string(
                self.FILTER_LIST,
                None,
                True
            ),
            ''
        )

    def test_complete_string_on_join(self):
        ''' Tests if empty string is returned when the join flag is set '''
        self.assertEqual(
            StubHadoopRepository().build_filter_string(self.FILTER_LIST, 'municipio'),
            self.EXPECTED
        )

class HadoopRepositoryBuildCriteriaTest(unittest.TestCase):
    ''' Tests simple criteria string builder '''
    def test_build_criteria_simple_op(self):
        ''' Tests if a simple op string is correctly built '''
        self.assertEqual(
            StubHadoopRepository().build_criteria(['eq','field','value']),
            'field = value'
        )

    def test_build_criteria_boolean_op(self):
        ''' Tests if a boolean op string is correctly built '''
        self.assertEqual(
            StubHadoopRepository().build_criteria(['nn','field']),
            'field IS NOT NULL'
        )
    
    def test_build_criteria_in_op(self):
        ''' Tests if a IN operator string is correctly built '''
        self.assertEqual(
            StubHadoopRepository().build_criteria(['in','field','a', 'b']),
            'field IN (a,b)'
        )

    def test_invoke_complex_criteria(self):
        ''' Tests if a complex op is correctly built '''
        self.assertEqual(
            StubHadoopRepository().build_criteria(['ltsz', 'column', 'value']),
            "LENGTH(CAST(column AS STRING)) < value"
        )
