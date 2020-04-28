
'''Main tests in API'''
import unittest
from test.stubs.repository import StubRepository

class StubRepositoryCustomPartition(StubRepository):
    ''' Fake repo to test instance methods '''
    DEFAULT_PARTITIONING = ''

class StubRepositoryCustomPartitionMultipleValues(StubRepository):
    ''' Fake repo to test instance methods '''
    DEFAULT_PARTITIONING = 'a, b, c'

class BaseRepositoryGeneralTest(unittest.TestCase):
    ''' General tests over StubRepo '''
    def test_table_name(self):
        ''' Verifica correta obtenção de nome de tabela '''
        repo = StubRepository()
        tbl_name = repo.get_table_name('MAIN')
        self.assertEqual(tbl_name, 'indicadores')

    def test_get_partitioning_empty(self):
        ''' Verifica correta obtenção de cláusula de partitioning quando não há
            particionamento especificado na classe '''
        repo = StubRepositoryCustomPartition()
        self.assertEqual(
            repo.replace_partition("min_part"),
            'MIN({val_field}) OVER() AS api_calc_{calc}'
        )

    def test_get_partitioning_default(self):
        ''' Verifica correta obtenção dde cláusula de particionamento '''
        repo = StubRepository()
        self.assertEqual(
            repo.replace_partition("min_part"),
            'MIN({val_field}) OVER(PARTITION BY {partition}) AS api_calc_{calc}'
        )

    def test_exclude_from_partition(self):
        ''' Verifica a correta exclusão do particionamento de campos inexistentes no SELECT '''
        repo = StubRepositoryCustomPartitionMultipleValues()
        self.assertEqual(repo.exclude_from_partition(['a'], ['count']), 'a')

class BaseRepositoryNamedQueryTest(unittest.TestCase):
    ''' Validates recovery of named query '''
    def test_validate_positive(self):
        ''' Verifica correta obtenção de named query '''
        repo = StubRepository()
        qry_name = repo.get_named_query('QRY_FIND_DATASET')
        self.assertEqual(qry_name, 'SELECT {} FROM {} {} {} {}')

    def test_validate_negative(self):
        ''' Verifica comportamento de obtenção de named query não mapeada '''
        repo = StubRepository()
        self.assertRaises(KeyError, repo.get_named_query, 'FAKE_QUERY')

class BaseRepositoryJoinSuffixTest(unittest.TestCase):
    ''' Validates recovery of join suffix '''
    def test_validate_positive(self):
        ''' Verifica correta obtenção de sufixo '''
        repo = StubRepository()
        sfx_name = repo.get_join_suffix('municipio')
        self.assertEqual(sfx_name, '_mun')

    def test_validate_negative(self):
        ''' Verifica comportamento de obtenção de sufixo não mapeado '''
        repo = StubRepository()
        self.assertRaises(KeyError, repo.get_join_suffix, 'galaxia')

class BaseRepositoryBuildAgrArrayTest(unittest.TestCase):
    ''' Classe que monta o array de valores agregados '''
    def test_invalid(self):
        ''' Retorna exceção quando a agregação é inválida '''
        vlr = 'vl_indicador'
        agr = ['sum', 'CSTM']
        repo = StubRepository()
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
        repo = StubRepository()
        result = repo.build_agr_array(vlr, agr)
        self.assertEqual(result, [])

    def test_empty_agregation(self):
        ''' Retorna string vazia se não houver agregação '''
        vlr = 'vl_indicador'
        agr = []
        repo = StubRepository()
        result = repo.build_agr_array(vlr, agr)
        self.assertEqual(result, [])

    def test_valid_agregation(self):
        ''' Retorna string vazia se não houver agregação '''
        vlr = 'vl_indicador'
        agr = ['sum', 'max', 'distinct']
        repo = StubRepository()
        result = repo.build_agr_array(vlr, agr)
        expected = [
            'sum(vl_indicador) AS agr_sum_vl_indicador',
            'max(vl_indicador) AS agr_max_vl_indicador'
        ]
        self.assertEqual(result, expected)

class BaseRepositoryBuildGenericAgrArrayTest(unittest.TestCase):
    ''' Classe que monta o array de valores agregados '''
    def test_invalid(self):
        ''' Retorna exceção quando a agregação é inválida '''
        agr = ['count', 'CSTM']
        repo = StubRepository()
        self.assertRaises(
            ValueError,
            repo.build_generic_agr_array,
            agr
        )

    def test_null_agregation(self):
        ''' Retorna string vazia se não houver agregação '''
        agr = None
        repo = StubRepository()
        result = repo.build_generic_agr_array(agr)
        self.assertEqual(result, [])

    def test_empty_agregation(self):
        ''' Retorna string vazia se não houver agregação '''
        agr = []
        repo = StubRepository()
        result = repo.build_generic_agr_array(agr)
        self.assertEqual(result, [])

    def test_valid_agregation(self):
        ''' Retorna string vazia se não houver agregação '''
        agr = ['count', 'sum', 'distinct']
        repo = StubRepository()
        result = repo.build_generic_agr_array(agr)
        expected = [
            'count(*) AS agr_count',
            'sum(*) AS agr_sum'
        ]
        self.assertEqual(result, expected)

class BaseRepositoryBuildOrderStringTest(unittest.TestCase):
    ''' Classe que monta o array de valores ordenados '''
    def test_invalid(self):
        ''' Retorna exceção quando a ordenação é inválida '''
        ordenacao = ['nm_indicador;select', 'nu_competencia']
        repo = StubRepository()
        self.assertRaises(
            ValueError,
            repo.build_order_string,
            ordenacao
        )

    def test_null_agregation(self):
        ''' Retorna string vazia se não houver ordenação '''
        ordenacao = None
        repo = StubRepository()
        result = repo.build_order_string(ordenacao)
        self.assertEqual(result, '')

    def test_empty_agregation(self):
        ''' Retorna string vazia se houver ordenação vazia '''
        ordenacao = []
        repo = StubRepository()
        result = repo.build_order_string(ordenacao)
        self.assertEqual(result, '')

    def test_valid_agregation(self):
        ''' Verifica string de retorno em condição válida '''
        ordenacao = ['nm_indicador', 'nu_competencia', '-vl_indicador']
        repo = StubRepository()
        result = repo.build_order_string(ordenacao)
        expected = 'ORDER BY nm_indicador, nu_competencia, vl_indicador DESC'
        self.assertEqual(result, expected)

class BaseRepositoryLoadAndPrepareTest(unittest.TestCase):
    ''' Classe que testa o carregamento do dao '''
    def test_valid(self):
        ''' Verifica declaração do método de carregamento do dao. '''
        repo = StubRepository()
        self.assertEqual(repo.get_dao(), 'Instanciei o DAO')

class BaseRepositoryBuildJoinedGroupStringTest(unittest.TestCase):
    ''' Classe de construção da cláusula do join '''
    def test_invalid_cats(self):
        ''' Lança erro ao tentar agrupar sem categoria. '''
        repo = StubRepository()
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
        repo = StubRepository()
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
        repo = StubRepository()
        cats = ['nm_indicador', 'lat_mun']
        agrs = ['nm_indicador']
        joined = 'municipio'
        result = repo.build_joined_grouping_string(cats, agrs, joined)
        self.assertEqual(result, 'GROUP BY nm_indicador, lat')

    def test_renamed_cat(self):
        ''' Check if rename is ignored when building grouping string '''
        repo = StubRepository()
        cats = ['nm_indicador', 'lat-latitude']
        agrs = ['nm_indicador']
        joined = 'municipio'
        result = repo.build_joined_grouping_string(cats, agrs, joined)
        self.assertEqual(result, 'GROUP BY nm_indicador, lat')

    def test_renamed_cat_joined(self):
        ''' Check if rename/suffix are ignored when building group string '''
        repo = StubRepository()
        cats = ['nm_indicador', 'lat_mun-latitude']
        agrs = ['nm_indicador']
        joined = 'municipio'
        result = repo.build_joined_grouping_string(cats, agrs, joined)
        self.assertEqual(result, 'GROUP BY nm_indicador, lat')

    def test_invalid_agregation(self):
        ''' Lança erro ao tentar agrupar sem join. '''
        repo = StubRepository()
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
        repo = StubRepository()
        cats = ['nm_indicador', 'lat_mun-latitude']
        agrs = ['distinct']
        joined = 'municipio'
        result = repo.build_joined_grouping_string(cats, agrs, joined)
        self.assertEqual(result, '')

class BaseRepositoryBuildFilterStringTest(unittest.TestCase):
    ''' Classe de construção da cláusula do join '''
    def test_no_where(self):
        ''' Retorna branco ao tentar filtrar sem where. '''
        repo = StubRepository()
        whrs = None
        is_on = False
        joined = None
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(result, '')

    def test_empty_where(self):
        ''' Retorna branco ao tentar filtrar com where vazio. '''
        repo = StubRepository()
        whrs = []
        is_on = False
        joined = None
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(result, '')

    def test_simple_valid(self):
        ''' Retorna cláusula where de consulta sem join. '''
        repo = StubRepository()
        whrs = ['eq-nu_competencia-2010', 'and', 'eq-cd_indicador-01_02_03_04']
        is_on = False
        joined = None
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(result, 'nu_competencia = 2010 and cd_indicador = 01_02_03_04')

    def test_hyphen_valid(self):
        ''' Retorna cláusula where de consulta sem join, com hífen. '''
        repo = StubRepository()
        whrs = ['eq-nu_competencia-2010', 'and', 'eq-cd_indicador-01\\-02\\-03\\-04']
        is_on = False
        joined = None
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(result, 'nu_competencia = 2010 and cd_indicador = 01-02-03-04')

    def test_in_clause(self):
        ''' Retorna cláusula where de consulta com cláusula IN. '''
        repo = StubRepository()
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
        repo = StubRepository()
        whrs = ['eq-nu_competencia-2010', 'and', 'eq-cd_indicador-01_02_03_04']
        is_on = False
        joined = 'municipio'
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(result, 'nu_competencia = 2010 and cd_indicador = 01_02_03_04')

    def test_valid_empty_where_join(self):
        ''' Retorna cláusula where vazia de consulta com join. '''
        repo = StubRepository()
        whrs = ['gt-lat_mun-0', 'gt-long_mun-0']
        is_on = False
        joined = 'municipio'
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(result, '')

    def test_valid_empty_on_join(self):
        ''' Retorna cláusula on vazia de consulta com join. '''
        repo = StubRepository()
        whrs = ['eq-nu_competencia-2010', 'eq-cd_indicador-01_02_03_04']
        is_on = True
        joined = 'municipio'
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(result, '')

    def test_valid_on_join(self):
        ''' Retorna cláusula on de consulta com join. '''
        repo = StubRepository()
        whrs = ['gt-lat_mun-0', 'gt-long_mun-0']
        is_on = True
        joined = 'municipio'
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(result, 'lat_mun > 0 long_mun > 0')

    def test_invalid_on_join(self):
        ''' Retorna cláusula where de consulta com join. '''
        repo = StubRepository()
        whrs = ['gt-lat_mun-0', 'gt-long_mun-0']
        is_on = True
        joined = None
        result = repo.build_filter_string(whrs, joined, is_on)
        self.assertEqual(result, '')

class BaseRepositoryBuildCategoriasTest(unittest.TestCase):
    ''' Classe de construção das categorias '''
    def test_no_cats(self):
        ''' Lança exceção quando não há categorias. '''
        repo = StubRepository()
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
        repo = StubRepository()
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
        repo = StubRepository()
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
        repo = StubRepository()
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
        repo = StubRepository()
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
        repo = StubRepository()
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

class BaseRepositoryBuildJoinedCategoriasTest(unittest.TestCase):
    ''' Classe de construção das categorias '''
    def test_no_cats(self):
        ''' Lança exceção quando não há categorias. '''
        repo = StubRepository()
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
        repo = StubRepository()
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
        repo = StubRepository()
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
        repo = StubRepository()
        cats = ['cd_indicador', 'nu_competencia', 'vl_indicador', 'lat_mun', 'long_mun']
        valor = ['vl_indicador']
        agregacao = None
        joined = 'municipio'
        result = repo.build_joined_categorias(cats, valor, agregacao, joined)
        self.assertEqual(result, 'cd_indicador, nu_competencia, vl_indicador, lat, long')

    def test_no_join(self):
        ''' Retorna normalmente quando não há join. '''
        repo = StubRepository()
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
        repo = StubRepository()
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
        repo = StubRepository()
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

class BaseRepositoryCombineValAggrTest(unittest.TestCase):
    ''' Classe de teste de combinações entre valor e agregação '''
    def test_one_val_one_aggr(self):
        ''' Um valor, uma agregação, sem sufixo. '''
        repo = StubRepository()
        valor = ['vl_indicador']
        agregacao = ['sum']
        result = repo.combine_val_aggr(valor, agregacao)
        self.assertEqual(result, ['sum(vl_indicador) AS agr_sum_vl_indicador'])

    def test_one_val_one_aggr_suffix(self):
        ''' Um valor, uma agregação, com sufixo. '''
        repo = StubRepository()
        valor = ['vl_indicador_mun']
        agregacao = ['sum']
        result = repo.combine_val_aggr(valor, agregacao, '_mun')
        self.assertEqual(result, ['sum(vl_indicador) AS agr_sum_vl_indicador'])

    def test_one_val_n_aggr(self):
        ''' Um valor, n agregações, sem sufixo. '''
        repo = StubRepository()
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
        repo = StubRepository()
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
        repo = StubRepository()
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
        repo = StubRepository()
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
        repo = StubRepository()
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
        repo = StubRepository()
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

class BaseRepositoryStdCalcsTest(unittest.TestCase):
    ''' Classe de teste de geração de string para cálculos com partitioning '''
    def test_std_calc_max(self):
        ''' Testa um cálculo de min e max '''
        options = {
            "valor": "vl_indicador",
            "calcs": ["min_part", "max_part"],
            "categorias": ["cd_mun_ibge", "nu_ano"]
        }
        repo = StubRepository()
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
        repo = StubRepository()
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
        repo = StubRepositoryCustomPartition()
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
        repo = StubRepositoryCustomPartitionMultipleValues()
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
        repo = StubRepository()
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
        repo = StubRepository()
        self.assertRaises(
            KeyError,
            repo.build_std_calcs,
            options
        )
