''' Services for query building and validation '''
class QueryBuilder():
    ''' Generic class for repositories '''
    @staticmethod
    def validate_field_array(fields):
        ''' Valida campos, evitando url injection '''
        chars = set(r'\;,')
        for field in fields:
            if any((c in chars) for c in field):
                return False
        return True

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
            blocking_cond = len([x for x in agregacao if x.upper() in blocking_aggr])
            if blocking_cond == 0:
                return f'GROUP BY {", ".join(nu_cats)}'
            return ''
        raise ValueError('Invalid aggregation (no value)')

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
