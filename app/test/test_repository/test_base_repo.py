'''Main tests in API'''
import unittest
from repository.base import BaseRepository

class BaseRepositoryValidateFieldArrayTest(unittest.TestCase):
    ''' Classe que testa a validação do field array '''
    def test_validate_positive(self):
        ''' Verifica positivo para separador de SQL '''
        fields = ['vl_indicador', 'cd_ibge;select']
        validation = BaseRepository.validate_field_array(fields)
        self.assertEqual(validation, False)

    def test_validate_negative(self):
        ''' Verifica negativo para separador de SQL '''
        fields = ['vl_indicador', 'cd_ibge']
        validation = BaseRepository.validate_field_array(fields)
        self.assertEqual(validation, True)

class BaseRepositoryTransformCategoriasTest(unittest.TestCase):
    ''' Classe que testa a validação do field array '''
    def test_validate_no_transform(self):
        ''' Verifica construção de categorias sem transformação '''
        categorias = ['vl_indicador', 'cd_ibge']
        expected = ['vl_indicador', 'cd_ibge']
        transformed = BaseRepository.transform_categorias(categorias)
        self.assertEqual(transformed, expected)

    def test_validate_all_transform(self):
        ''' Verifica construção de categorias com transformação em todos '''
        categorias = ['vl_indicador-valor', 'cd_ibge-local']
        expected = ['vl_indicador AS valor', 'cd_ibge AS local']
        transformed = BaseRepository.transform_categorias(categorias)
        self.assertEqual(transformed, expected)

    def test_validate_semi_transform(self):
        ''' Verifica construção de categorias com transformação em parte '''
        categorias = ['vl_indicador-valor', 'cd_ibge']
        expected = ['vl_indicador AS valor', 'cd_ibge']
        transformed = BaseRepository.transform_categorias(categorias)
        self.assertEqual(transformed, expected)

class BaseRepositoryCatchInjectionTest(unittest.TestCase):
    ''' Classe que verifica palavras-chave do SQL que indiquem uma
        injeção de SQL '''
    def test_validate_positive(self):
        ''' Verifica positivo para palavras-chave de SQL '''
        categorias = ["vl_indicador", "cd_ibgeselect"]
        options = {"categorias": categorias}
        validation = BaseRepository.catch_injection(options)
        self.assertEqual(validation, True)

    def test_validate_positive_complex(self):
        ''' Verifica positivo para palavras-chave de SQL '''
        categorias = ["vl_indicador", "cd_ibge-truncate"]
        options = {"categorias": categorias}
        validation = BaseRepository.catch_injection(options)
        self.assertEqual(validation, True)

    def test_validate_negative(self):
        ''' Verifica negativo para palavras-chave de SQL '''
        categorias = ["vl_indicador", "cd_ibge"]
        options = {"categorias": categorias}
        validation = BaseRepository.catch_injection(options)
        self.assertEqual(validation, False)

    def test_validate_negative_empty(self):
        ''' Verifica negativo para atributo vazio '''
        categorias = ["vl_indicador", "cd_ibge"]
        options = {
            "categorias": categorias,
            "valor": []
        }
        validation = BaseRepository.catch_injection(options)
        self.assertEqual(validation, False)

    def test_validate_negative_null(self):
        ''' Verifica negativo para atributo nulo '''
        categorias = ["vl_indicador", "cd_ibge"]
        options = {
            "categorias": categorias,
            "valor": None
        }
        validation = BaseRepository.catch_injection(options)
        self.assertEqual(validation, False)

class BaseRepositoryPrependAggregationsTest(unittest.TestCase):
    ''' Classe que verifica a montagem de campos genéricos de agegação '''
    def test_prepend_aggregations_valid(self):
        ''' Retorna distinct, dentre outras agregações enviadas '''
        aggrs = ['SUM', 'DISTINCT', 'MAX']
        result = BaseRepository.prepend_aggregations(aggrs)
        self.assertEqual(result, ['DISTINCT'])

    def test_prepend_aggregations_empty(self):
        ''' Retorna lista vazia, pois não tem agregação genérica '''
        aggrs = ['SUM', 'MAX']
        result = BaseRepository.prepend_aggregations(aggrs)
        self.assertEqual(result, [])

    def test_prepend_aggregations_void(self):
        ''' Retorna lista vazia quando recebe agregação vazia '''
        aggrs = []
        result = BaseRepository.prepend_aggregations(aggrs)
        self.assertEqual(result, [])

    def test_prepend_aggregations_none(self):
        '''Retorna lista vazia quando recebe agregações nulas '''
        aggrs = None
        result = BaseRepository.prepend_aggregations(aggrs)
        self.assertEqual(result, [])

class BaseRepositoryTransformJoindeCategoriasTest(unittest.TestCase):
    ''' Classe que verifica a montagem de campos de categoria
        em query com join '''
    def test_all_joined_no_as(self):
        ''' Retorna todas categorias transformadas sem rename '''
        categorias = ['nm_indicador_mun', 'vl_indicador_mun']
        result = BaseRepository.transform_joined_categorias(categorias, '_mun')
        self.assertEqual(result, ['nm_indicador', 'vl_indicador'])

    def test_all_joined_some_as(self):
        ''' Retorna categorias transformadas, algumas com rename '''
        categorias = ['nm_indicador_mun-nome', 'vl_indicador_mun']
        result = BaseRepository.transform_joined_categorias(categorias, '_mun')
        self.assertEqual(result, ['nm_indicador AS nome', 'vl_indicador'])

    def test_some_joined_some_as(self):
        ''' Retorna categorias transformadas, algumas com rename '''
        categorias = ['nm_indicador-nome', 'vl_indicador_mun-valor',
                      'ds_indicador', 'cd_indicador_mun']
        result = BaseRepository.transform_joined_categorias(categorias, '_mun')
        expected = ['nm_indicador AS nome', 'vl_indicador AS valor',
                    'ds_indicador', 'cd_indicador']
        self.assertEqual(result, expected)

class BaseRepositoryBuildGroupingStringTest(unittest.TestCase):
    ''' Classe que verifica a montagem de campos de group by '''
    def test_void_categories(self):
        ''' Retorna exceção quando não há categorias para agrupar '''
        cats = None
        agrs = ['SUM', 'MAX', 'DISTINCT']
        self.assertRaises(
            ValueError,
            BaseRepository.build_grouping_string,
            cats,
            agrs
        )

    def test_empty_categories(self):
        ''' Retorna exceção quando há categorias vazias para agrupar '''
        cats = []
        agrs = ['SUM', 'MAX', 'DISTINCT']
        self.assertRaises(
            ValueError,
            BaseRepository.build_grouping_string,
            cats,
            agrs
        )

    def test_invalid_agregation(self):
        ''' Retorna exceção quando não há agregação para agrupar '''
        cats = ['nm_indicador', 'nu_competencia']
        agrs = None
        self.assertRaises(
            ValueError,
            BaseRepository.build_grouping_string,
            cats,
            agrs
        )

    def test_empty_agregation(self):
        ''' Retorna exceção quando há agregação vazia para agrupar '''
        cats = ['nm_indicador', 'nu_competencia']
        agrs = []
        self.assertRaises(
            ValueError,
            BaseRepository.build_grouping_string,
            cats,
            agrs
        )

    def test_renamed_cats(self):
        ''' Retorna exceção quando não há agregação para agrupar '''
        cats = ['nm_indicador-nome', 'nu_competencia']
        agrs = ['SUM', 'MAX']
        result = BaseRepository.build_grouping_string(cats, agrs)
        self.assertEqual(result, 'GROUP BY nm_indicador, nu_competencia')

    def test_with_distinct(self):
        ''' Retorna exceção quando não há agregação para agrupar '''
        cats = ['nm_indicador-nome', 'nu_competencia']
        agrs = ['SUM', 'MAX', 'DISTINCT']
        result = BaseRepository.build_grouping_string(cats, agrs)
        self.assertEqual(result, '')

class BaseRepositoryGetAgrStringTest(unittest.TestCase):
    ''' Classe que verifica a montagem de um campo de agregação '''
    def test_invalid(self):
        ''' Retorna exceção quando a agregação é inválida '''
        vlr = 'vl_indicador'
        agr = 'CSTM'
        self.assertRaises(
            ValueError,
            BaseRepository.get_agr_string,
            agr,
            vlr
        )

    def test_bypass(self):
        ''' Verifica se retorna None quando a agregação está na
            lista de ignore '''
        vlr = 'vl_indicador'
        agr = 'DISTINCT'
        result = BaseRepository.get_agr_string(agr, vlr)
        self.assertEqual(result, None)

    def test_as_is(self):
        ''' Verifica se retorna corretamente uma agregação que
            está na lista as_is '''
        vlr = 'vl_indicador'
        agr = 'sum'
        expected = 'sum(vl_indicador) AS agr_sum_vl_indicador'
        result = BaseRepository.get_agr_string(agr, vlr)
        self.assertEqual(result, expected)

    def test_custom(self):
        ''' Verifica se retorna corretamente uma agregação que
            não está na lista as_is '''
        vlr = 'vl_indicador'
        agr = 'pct_count'
        result = BaseRepository.get_agr_string(agr, vlr)
        expected = ('COUNT(vl_indicador) * 100 / SUM(COUNT(vl_indicador)) '
                    'OVER() AS agr_pct_count_vl_indicador')
        self.assertEqual(result, expected)

    def test_rank_count(self):
        ''' Verifica se retorna corretamente uma agregação RANK_COUNT '''
        vlr = 'vl_indicador'
        agr = 'rank_count'
        result = BaseRepository.get_agr_string(agr, vlr)
        expected = 'RANK() OVER(ORDER BY COUNT(vl_indicador) DESC) AS agr_rank_count_vl_indicador'
        self.assertEqual(result, expected)

    def test_rank_dense_count(self):
        ''' Verifica se retorna corretamente uma agregação RANK_DENSE_COUNT '''
        vlr = 'vl_indicador'
        agr = 'rank_dense_count'
        result = BaseRepository.get_agr_string(agr, vlr)
        expected = ('DENSE_RANK() OVER(ORDER BY COUNT(vl_indicador) DESC) AS '
                    'agr_rank_dense_count_vl_indicador')
        self.assertEqual(result, expected)

    def test_rank_sum(self):
        ''' Verifica se retorna corretamente uma agregação RANK_SUM '''
        vlr = 'vl_indicador'
        agr = 'rank_sum'
        result = BaseRepository.get_agr_string(agr, vlr)
        expected = ('RANK() OVER(ORDER BY SUM(vl_indicador) DESC) AS '
                    'agr_rank_sum_vl_indicador')
        self.assertEqual(result, expected)

    def test_rank_dense_sum(self):
        ''' Verifica se retorna corretamente uma agregação RANK_DENSE_SUM '''
        vlr = 'vl_indicador'
        agr = 'rank_dense_sum'
        result = BaseRepository.get_agr_string(agr, vlr)
        expected = ('DENSE_RANK() OVER(ORDER BY SUM(vl_indicador) DESC) AS '
                    'agr_rank_dense_sum_vl_indicador')
        self.assertEqual(result, expected)

class BaseRepositoryValidateClauseTest(unittest.TestCase):
    ''' Classe que valida uma cláusula do filtro '''
    def test_valid_no_join(self):
        ''' Sinaliza positivamente quando não é um join '''
        result = BaseRepository.validate_clause(['eq', 'any'], None, None, None)
        self.assertEqual(result, True)

    def test_valid_join_com_sufixo(self):
        ''' Sinaliza positivamente quando é um filtro de join
            e tem um sufixo '''
        result = BaseRepository.validate_clause(['eq', 'any_mun'], 'municipio', True, '_mun')
        self.assertEqual(result, True)

    def test_valid_out_join_sem_sufixo(self):
        ''' Sinaliza positivamente quando é um filtro fora do
            join e não tem um sufixo '''
        result = BaseRepository.validate_clause(['eq', 'any'], 'municipio', False, '_mun')
        self.assertEqual(result, True)

    def test_invalid_join_sem_sufixo(self):
        ''' Sinaliza negativamente quando é um filtro de join
            e não tem um sufixo '''
        result = BaseRepository.validate_clause(['eq', 'any'], 'municipio', True, '_mun')
        self.assertEqual(result, False)

    def test_invalid_out_join_sufixo(self):
        ''' Sinaliza negativamente quando é um filtro fora do
            join e tem um sufixo '''
        result = BaseRepository.validate_clause(['eq', 'any_mun'], 'municipio', False, '_mun')
        self.assertEqual(result, False)
