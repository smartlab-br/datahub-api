''' Repository genérico '''
from impala.util import as_pandas
from datasources import get_hive_connection, get_impala_connection

#pylint: disable=R0903
class BaseRepository(object):
    ''' Generic class for repositories '''
    NAMED_QUERIES = {
        'QRY_FIND_DATASET': 'SELECT {} FROM {} {} {} {} {} {}',
        'QRY_FIND_JOINED_DATASET': 'SELECT {} FROM {} LEFT JOIN {} ON {} {} {} {}'
    }
    TABLE_NAMES = {}
    ON_JOIN = {}
    JOIN_SUFFIXES = {}
    VAL_FIELD = 'vl_indicador'
    DEFAULT_GROUPING = 'nu_competencia, cd_indicador'
    DEFAULT_PARTITIONING = 'cd_indicador'
    CALCS_DICT = {
        "min_part": 'MIN({val_field}) OVER(PARTITION BY {partition}) AS api_calc_{calc}',
        "max_part": 'MAX({val_field}) OVER(PARTITION BY {partition}) AS api_calc_{calc}',
        "avg_part": 'AVG({val_field}) OVER(PARTITION BY {partition}) AS api_calc_{calc}',
        "var_part": ('{val_field} - AVG({val_field}) OVER(PARTITION BY {partition}) '
                     'AS api_calc_{calc}'
                    ),
        "ln_var_part": ('LOG10({val_field} - AVG({val_field}) OVER(PARTITION BY {partition}) / '
                        'AVG({val_field}) OVER(PARTITION BY {partition}) + 1.0001) '
                        'AS api_calc_{calc}'
                       ),
        "norm_pos_part": ('CASE '
                            '(MAX({val_field}) OVER(PARTITION BY {partition}) - '
                                'MIN({val_field}) OVER(PARTITION BY {partition})) '
                          'WHEN 0 '
                          'THEN 0.5 '
                          'ELSE '
                          '({val_field} - MIN({val_field}) OVER(PARTITION BY {partition})) / '
                            '(MAX({val_field}) OVER(PARTITION BY {partition}) - '
                                'MIN({val_field}) OVER(PARTITION BY {partition})) '
                          'END '
                          'AS api_calc_{calc}'
                         ),
        "ln_norm_pos_part": ('CASE '
                                '(MAX({val_field}) OVER(PARTITION BY {partition}) - '
                                    'MIN({val_field}) OVER(PARTITION BY {partition})) '
                             'WHEN 0 '
                             'THEN LOG10(1.5) '
                             'ELSE '
                                'LOG10(({val_field} - MIN({val_field}) '
                                    'OVER(PARTITION BY {partition})) / '
                                    '(MAX({val_field}) OVER(PARTITION BY {partition}) - '
                                    'MIN({val_field}) OVER(PARTITION BY {partition})) + 1.0001) '
                             'END '
                             'AS api_calc_{calc}'
                            ),
        "norm_part": ('CASE WHEN {val_field} >= 0 '
                      'THEN {val_field} / (MAX({val_field}) OVER(PARTITION BY {partition})) '
                      'ELSE -1 * {val_field} / (MIN({val_field}) '
                      'OVER(PARTITION BY {partition})) '
                      'END AS api_calc_{calc}'
                     ),
        "ln_norm_part": ('CASE WHEN {val_field} >= 0 '
                         'THEN LOG10({val_field} / '
                         '(MAX({val_field}) OVER(PARTITION BY {partition})) + 1.0001) '
                         'ELSE -1 * LOG10({val_field} / '
                         '(MIN({val_field}) OVER(PARTITION BY {partition})) + 1.0001) '
                         'END AS api_calc_{calc}'
                        )
    }

    def __init__(self):
        ''' Construtor '''
        self.dao = self.load_and_prepare()

    def get_dao(self):
        ''' Garantia de que o modelo estará carregado '''
        if self.dao is None:
            self.load_and_prepare()
        return self.dao

    @staticmethod
    def validate_field_array(fields):
        ''' Valida campos, evitando url injection '''
        chars = set(r'\;,')
        for field in fields:
            if any((c in chars) for c in field):
                return False
        return True

    def build_agr_array(self, valor=None, agregacao=None):
        ''' Combina a agregação com o campo de valor, para juntar nos campos da query '''
        if agregacao is None or not agregacao:
            return []
        result = []
        for each_aggr in agregacao:
            agr_string = self.get_agr_string(each_aggr, valor)
            if agr_string is not None:
                result.append(agr_string)
        return result

    def build_generic_agr_array(self, agregacao=None):
        ''' Prepara agregação sem campo definido '''
        if agregacao is None or not agregacao:
            return []
        result = []
        for each_aggr in agregacao:
            agr_string = self.get_agr_string(each_aggr, '*')
            if agr_string is not None:
                result.append(agr_string)
        return result

    def build_order_string(self, ordenacao=None):
        ''' Prepara ordenação '''
        if ordenacao is None or not ordenacao:
            return ''
        if not self.validate_field_array(ordenacao):
            raise ValueError('Invalid aggregation')
        order_str = ''
        for field in ordenacao:
            if order_str == '':
                order_str += 'ORDER BY '
            else:
                order_str += ', '
            if "-" in field:
                order_str += field[1:] + ' DESC'
            else:
                order_str += field
        return order_str

    @staticmethod
    def get_agr_string(agregacao=None, valor=None):
        ''' Obtém o alias de uma função, se fora do pardão '''
        as_is = ['SUM', 'COUNT', 'MAX', 'MIN', 'AVG']
        ignore = ['DISTINCT']
        if agregacao.upper() in ignore:
            return None
        result = ''

        if agregacao.upper() in as_is:
            result = (f'{agregacao}({valor}) AS agr_{agregacao}'
                      f'{("_" +valor) if valor != "*" else ""}')
        elif agregacao.upper() == 'PCT_COUNT':
            result = (f'COUNT({valor}) * 100 / SUM(COUNT({valor})) OVER() AS '
                      f'agr_{agregacao}{("_" +valor) if valor != "*" else ""}')
        elif agregacao.upper() == 'PCT_SUM':
            result = (f'SUM({valor}) * 100 / SUM({valor}) OVER() AS '
                      f'agr_{agregacao}{("_" +valor) if valor != "*" else ""}')
        elif agregacao.upper() == 'RANK_COUNT':
            result = (f'RANK() OVER(ORDER BY COUNT({valor}) DESC) AS '
                      f'agr_{agregacao}{("_" +valor) if valor != "*" else ""}')
        elif agregacao.upper() == 'RANK_DENSE_COUNT':
            result = (f'DENSE_RANK() OVER(ORDER BY COUNT({valor}) DESC) AS '
                      f'agr_{agregacao}{("_" +valor) if valor != "*" else ""}')
        elif agregacao.upper() == 'RANK_SUM':
            result = (f'RANK() OVER(ORDER BY SUM({valor}) DESC) AS '
                      f'agr_{agregacao}{("_" +valor) if valor != "*" else ""}')
        elif agregacao.upper() == 'RANK_DENSE_SUM':
            result = (f'DENSE_RANK() OVER(ORDER BY SUM({valor}) DESC) AS '
                      f'agr_{agregacao}{("_" +valor) if valor != "*" else ""}')
        else:
            raise ValueError('Invalid aggregation')
        return result

    @staticmethod
    def get_simple_agr_string(agregacao=None, valor=None):
        ''' Obtém o alias de uma função, se fora do pardão '''
        as_is = ['SUM', 'COUNT', 'MAX', 'MIN', 'AVG']
        ignore = ['DISTINCT']
        if agregacao.upper() in ignore:
            return None
        result = ''

        if agregacao.upper() in as_is:
            result = f'{agregacao}({valor})'
        else:
            raise ValueError('Invalid aggregation for calcs')
        return result

    @staticmethod
    def build_grouping_string(categorias=None, agregacao=None):
        ''' Constrói o tracho da query que comanda o agrupamento '''
        if categorias is None or not categorias:
            raise ValueError('Invalid fields')
        nu_cats = []
        for categoria in categorias:
            if '-' in categoria:
                arr_categoria = categoria.split('-')
                nu_cats.append(arr_categoria[0])
            else:
                nu_cats.append(categoria)
        if agregacao is not None and agregacao:
            blocking_aggr = ['DISTINCT']
            blocking_cond = len(list(set([x.upper() for x in agregacao]) & set(blocking_aggr)))
            if blocking_cond == 0:
                return f'GROUP BY {", ".join(nu_cats)}'
            return ''
        raise ValueError('Invalid aggregation (no value)')

    def build_joined_grouping_string(self, categorias=None, agregacao=None, joined=None):
        ''' Constrói o tracho da query que comanda o agrupamento '''
        if categorias is None:
            raise ValueError('Invalid fields')
        nu_cats = []
        for categoria in categorias:
            suffix = self.get_join_suffix(joined)
            if '-' in categoria:
                arr_categoria = categoria.split('-')
                if arr_categoria[0][-len(suffix):] == suffix:
                    nu_cats.append(arr_categoria[0][:-len(suffix)])
                else:
                    nu_cats.append(arr_categoria[0])
            elif categoria[-len(suffix):] == suffix:
                nu_cats.append(categoria[:-len(suffix)])
            else:
                nu_cats.append(categoria)
        if agregacao is not None:
            blocking_aggr = ['DISTINCT']
            blocking_cond = len(list(set([x.upper() for x in agregacao]) & set(blocking_aggr)))
            if blocking_cond == 0:
                return f'GROUP BY {", ".join(nu_cats)}'
            return ''
        raise ValueError('Invalid aggregation (no value)')

    def load_and_prepare(self):
        ''' Método abstrato para carregamento do dataset '''
        raise NotImplementedError("Repositórios precisam implementar load_and_prepare")

    def get_named_query(self, query_name):
        ''' Obtém uma string parametrizada de query '''
        qry_dict = self.NAMED_QUERIES
        return qry_dict[query_name]

    def get_table_name(self, table_name):
        ''' Obtém o nome de uma tabela do cloudera '''
        tbl_dict = self.TABLE_NAMES
        if table_name in tbl_dict:
            return tbl_dict[table_name]
        raise KeyError("Invalid theme")

    def get_join_condition(self, table_name, join_clauses=None):
        ''' Obtém a condição do join das tabelas '''
        main_join = self.ON_JOIN[table_name]
        if join_clauses is None:
            return main_join
        # COMPOSIÇÃO DO JOIN COM FILTRO DESATIVADO
        # joined_filters = self.build_filter_string(join_clauses, table_name, True)
        # if joined_filters is None or joined_filters == '':
        #     return main_join
        # return main_join + ' AND ' + joined_filters
        return main_join

    def get_join_suffix(self, table_name):
        ''' Obtém uma string de sufixo de campo de tabela juntada '''
        on_suffix_dict = self.JOIN_SUFFIXES
        return on_suffix_dict[table_name]

    def build_categorias(self, categorias, options):
        ''' Constrói a parte dos atributos selecionados na query '''
        if not self.check_params(options, ['categorias']):
            raise ValueError('Invalid Categories - required')
        categorias = self.transform_categorias(categorias)
        prepended_aggr = self.prepend_aggregations(options['agregacao'])
        str_calcs = ''
        if self.check_params(options, ['calcs']):
            calcs_options = options.copy()
            calcs_options['categorias'] = categorias
            str_calcs += self.build_std_calcs(calcs_options)
        if self.check_params(options, ['agregacao', 'valor']):
            tmp_cats = self.combine_val_aggr(options['valor'], options['agregacao'])
            if not isinstance(tmp_cats, list):
                categorias += tmp_cats.split(", ")
            else:
                categorias += tmp_cats
        elif (not self.check_params(options, ['agregacao']) and
              self.check_params(options, ['valor'])):
            categorias += options['valor']
        elif (self.check_params(options, ['agregacao']) and
              not self.check_params(options, ['valor'])):
            categorias += self.build_generic_agr_array(options['agregacao'])
        if self.validate_field_array(categorias) and self.validate_field_array(prepended_aggr):
            if 'calcs' not in options or options['calcs'] is None or str_calcs == '':
                return ' '.join(prepended_aggr) + ' ' + ', '.join(categorias)
            return ' '.join(prepended_aggr) + ' ' + ', '.join(categorias) + ', ' + str_calcs
        raise ValueError('Invalid attributes')

    def build_std_calcs(self, options):
        '''Constrói campos calculados de valor, como min, max e normalizado '''
        if self.VAL_FIELD is None or self.get_default_partitioning(options) is None:
            return ''

        # Pega o valor passado ou padrão, para montar a query
        val_field = self.VAL_FIELD
        if self.check_params(options, ['valor']):
            val_field = options['valor']

        # Pega o valor do particionamento
        if not self.check_params(options, ['partition']):
            if self.get_default_partitioning(options) != '':
                res_partition = self.get_default_partitioning(options)
            else:
                res_partition = "'1'"
        else:
            res_partition = options['partition']

        # Transforma o campo de valor em campo agregado conforme query
        if self.check_params(options, ['agregacao']):
            val_field = self.get_simple_agr_string(options['agregacao'][0], options['valor'][0])
            if self.check_params(options, ['pivot']):
                res_partition = self.exclude_from_partition(
                    options['categorias'],
                    options['agregacao']
                )

        str_res_partition = res_partition
        if isinstance(res_partition, list):
            str_res_partition = ",".join(res_partition)
        
        # Constrói a query
        arr_calcs = []
        for calc in options['calcs']:
            # Always appends min and max when calc is not one of them
            if calc not in ['min_part', 'max_part']:
                arr_calcs.append(
                    self.replace_partition('min_part').format(
                        val_field=val_field,
                        partition=str_res_partition,
                        calc='min_part'
                    )
                )
                arr_calcs.append(
                    self.replace_partition('max_part').format(
                        val_field=val_field,
                        partition=str_res_partition,
                        calc='max_part'
                    )
                )
            # Resumes identification of calc
            arr_calcs.append(
                self.replace_partition(calc).format(
                    val_field=val_field,
                    partition=str_res_partition,
                    calc=calc
                )
            )
        return ', '.join(arr_calcs)

    def replace_partition(self, qry_part):
        ''' Changes OVER clause when there's no partitioning '''
        if self.get_default_partitioning(options) == '':
            return self.CALCS_DICT[qry_part].replace("PARTITION BY {partition}", "")
        return self.CALCS_DICT[qry_part]

    def exclude_from_partition(self, categorias, agregacoes):
        ''' Remove do partition as categorias não geradas pela agregação '''
        partitions = self.get_default_partitioning(options).split(", ")
        groups = self.build_grouping_string(categorias, agregacoes).replace('GROUP BY ', '').split(", ")
        result = []
        for partition in partitions:
            if partition in groups:
                result.append(partition)
        return ", ".join(result)
    
    def get_default_partitioning(self, options):
        return self.DEFAULT_PARTITIONING

    def combine_val_aggr(self, valor, agregacao, suffix=None):
        ''' Combina valores e agregções para construir a string correta '''
        if len(valor) == 1:
            if suffix is not None and valor[0][-len(suffix):] == suffix:
                return self.build_agr_array(valor[0][:-len(suffix)], agregacao)
            return self.build_agr_array(valor[0], agregacao)
        result = ''
        for indx, val in enumerate(valor):
            if indx > 0:
                result += ', '
            aux_val = val
            if suffix is not None and val[-len(suffix):] == suffix:
                aux_val = val[:-len(suffix)]
            if len(agregacao) == 1:
                agrs = agregacao[0].split('-')
                result += ', '.join(self.build_agr_array(aux_val, agrs))
            else:
                agrs = agregacao[indx].split('-')
                result += ', '.join(self.build_agr_array(aux_val, agrs))
        return result

    @staticmethod
    def transform_categorias(categorias):
        ''' Regula a mudança de nome de campos '''
        result = []
        for categoria in categorias:
            if '-' in categoria:
                arr_categoria = categoria.split('-')
                result.append(arr_categoria[0] + ' AS ' + arr_categoria[1])
            else:
                result.append(categoria)
        return result

    @staticmethod
    def transform_joined_categorias(categorias, suffix):
        ''' Regula a mudança de nome de campos '''
        result = []
        for categoria in categorias:
            if '-' in categoria:
                arr_categoria = categoria.split('-')
                if arr_categoria[0][-len(suffix):] == suffix:
                    result.append(arr_categoria[0][:-len(suffix)] + ' AS ' + arr_categoria[1])
                else:
                    result.append(arr_categoria[0] + ' AS ' + arr_categoria[1])
            else:
                if categoria[-len(suffix):] == suffix:
                    result.append(categoria[:-len(suffix)])
                else:
                    result.append(categoria)
        return result

    @staticmethod
    def prepend_aggregations(agregacoes):
        ''' Monta qualificadores pré-campos do SELECT '''
        if agregacoes is None:
            return []
        possible_prepends = ['DISTINCT']
        valid_prepends = []
        for agregacao in agregacoes:
            if agregacao.upper() in possible_prepends:
                valid_prepends.append(agregacao)
        return valid_prepends

    def build_joined_categorias(self, categorias, valor=None, agregacao=None,
                                joined=None):
        ''' Constrói a parte dos atributos selecionados na query '''
        if categorias is None or not categorias:
            raise ValueError('Invalid Categories - required')
        str_cat = []
        suffix = self.get_join_suffix(joined)
        str_cat += self.transform_joined_categorias(categorias, suffix)
        if agregacao is not None and valor is not None:
            str_cat += self.combine_val_aggr(valor, agregacao, suffix)
        elif agregacao is not None and valor is None:
            str_cat += self.build_generic_agr_array(agregacao)
        if self.validate_field_array(str_cat):
            return ', '.join(str_cat)
        raise ValueError('Invalid attributes')

    def build_filter_string(self, where=None, joined=None, is_on=False):
        ''' Builds WHERE clauses or added ON conditions '''
        simple_operators = {
            'EQ': "=", "NE": "!=", "LE": "<=", "LT": "<", "GE": ">=",
            "GT": ">", "LK": "LIKE"
        }
        boolean_operators = {
            "NL": "IS NULL", "NN": "IS NOT NULL"
        }
        suffix = ''
        if joined is not None:
            suffix = self.get_join_suffix(joined)
        if where is None or (joined is None and is_on):
            return ''
        arr_result = []
        for each_clause in where:
            w_clause = each_clause.replace('\\-', '|')
            w_clause = w_clause.split('-')
            w_clause = [f.replace('|', '-') for f in w_clause]
            if w_clause[0].upper() == 'AND' or w_clause[0].upper() == 'OR':
                arr_result.append(w_clause[0])
            elif self.validate_clause(w_clause, joined, is_on, suffix):
                if w_clause[0].upper() in simple_operators:
                    arr_result.append(
                        f'{w_clause[1]} '
                        f'{simple_operators[w_clause[0].upper()]} '
                        f'{w_clause[2]}'
                    )
                elif w_clause[0].upper() in boolean_operators:
                    arr_result.append(
                        f'{w_clause[1]} '
                        f'{boolean_operators[w_clause[0].upper()]}'
                    )
                elif w_clause[0].upper() == 'IN':
                    arr_result.append(f'{w_clause[1]} IN ({",".join(w_clause[2:])})')
        return ' '.join(arr_result)

    @staticmethod
    def check_params(options, params):
        ''' Checks if param exists in options '''
        for param in params:
            if param not in options or options[param] is None or not options[param]:
                return False
        return True

    @staticmethod
    def validate_clause(clause, joined, is_on, suffix):
        ''' Valida a construção da cláusula do where ou do on '''
        if joined is None:
            return True
        if joined is not None and is_on and clause[1][-len(suffix):] == suffix:
            return True
        if joined is not None and not is_on and clause[1][-len(suffix):] != suffix:
            return True
        return False

    @staticmethod
    def catch_injection(options):
        ''' Verifica se há alguma palavra reservada indicando SQL Injection '''
        blocked_words = ['SELECT', 'JOIN', 'UNION', 'WHERE', 'ALTER', 'CREATE',
                         'TRUNCATE', 'DELETE', 'CONCAT', 'UPDATE', 'FROM', ';',
                         '|']
        for key, option in options.items():
            if option is not None and key not in ['no_wrap', 'as_pandas', 'as_dict']:
                checked_words = ','.join(option).upper()
                if key in ['limit', 'offset']:
                    checked_words = option.upper()
                if any(blk in checked_words for blk in blocked_words):
                    return True
        return False

class HadoopRepository(BaseRepository):
    '''Generic class for hive repositories '''
    def load_and_prepare(self):
        ''' Método abstrato para carregamento do dataset '''
        raise NotImplementedError("Repositórios precisam implementar load_and_prepare")

    def fetch_data(self, query):
        ''' Runs the query in pandas '''
        cursor = self.get_dao().cursor()
        cursor.execute(query)
        return as_pandas(cursor)

    def find_dataset(self, options=None):
        ''' Obtém dataset de acordo com os parâmetros informados '''
        if self.catch_injection(options):
            raise ValueError('SQL reserved words not allowed!')
        str_where = ''
        if options['where'] is not None:
            str_where = ' WHERE ' + self.build_filter_string(options['where'])
        str_group = ''
        nu_cats = options['categorias']
        if options['pivot'] is not None:
            nu_cats = nu_cats + options['pivot']
        if options['agregacao'] is not None and options['agregacao']:
            str_group = self.build_grouping_string(
                nu_cats,
                options['agregacao']
            )
        str_categorias = self.build_categorias(nu_cats, options)
        str_limit = ''
        if options['limit'] is not None:
            str_limit = f'LIMIT {options["limit"]}'
        str_offset = ''
        if options['offset'] is not None:
            str_offset = f'OFFSET {options["offset"]}'
        if 'theme' not in options:
            options['theme'] = 'MAIN'
        query = self.get_named_query('QRY_FIND_DATASET').format(
            str_categorias,
            self.get_table_name(options['theme']),
            str_where,
            str_group,
            self.build_order_string(options['ordenacao']),
            str_limit,
            str_offset
        )
        return self.fetch_data(query)

    def find_joined_dataset(self, options=None):
        ''' Obtém dataset de acordo com os parâmetros informados '''
        if self.catch_injection(options):
            raise ValueError('SQL reserved words not allowed!')
        if options['joined'] is None:
            raise ValueError('Joined table is required')
        str_where = ''
        if options['where'] is not None:
            str_where = ' WHERE ' + self.build_filter_string(options['where'], options['joined'],
                                                             False)
        str_group = ''
        if options['agregacao'] is not None:
            str_group = self.build_joined_grouping_string(
                options['categorias'],
                options['agregacao'],
                options['joined']
            )
        if 'theme' not in options:
            options['theme'] = 'MAIN'
        str_categorias = self.build_joined_categorias(options['categorias'], options['valor'],
                                                      options['agregacao'], options['joined'])
        query = self.get_named_query('QRY_FIND_JOINED_DATASET').format(
            str_categorias,
            self.get_table_name(options['theme']), # FROM
            self.get_table_name(options['joined']), # JOIN
            self.get_join_condition(options['joined'], options['where']), # ON
            str_where, # WHERE
            str_group, # GROUP BY
            self.build_order_string(options['ordenacao']) # ORDER BY
        )

        return self.fetch_data(query)

class HiveRepository(HadoopRepository):
    '''Generic class for hive repositories '''
    def load_and_prepare(self):
        ''' Prepara o DAO '''
        self.dao = get_hive_connection()

class ImpalaRepository(HadoopRepository):
    '''Generic class for hive repositories '''
    def load_and_prepare(self):
        ''' Prepara o DAO '''
        self.dao = get_impala_connection()
