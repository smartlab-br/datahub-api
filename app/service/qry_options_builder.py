''' Service para conversão de atributos de query para os objetos do fetch '''
class QueryOptionsBuilder():
    ''' Classe de serviço '''
    @classmethod
    def build_options(cls, r_args, rules='query'):
        ''' Constrói as opções da pesquisa '''
        if isinstance(r_args, dict):
            options = r_args.copy()
        else:
            options = r_args.copy().to_dict(flat=False)

        categorias = cls.extract_qry_param(r_args, 'categorias')
        if categorias is None:
            if rules in ['query']:
                raise ValueError('Categories required')
        else:
            options['categorias'] = categorias

        if r_args.get('filtros') is not None:
            filtros = r_args.get('filtros').replace('\\,', '|')
            filtros = filtros.split(',')
            filtros = [f.replace('|', ',') for f in filtros]
            options['where'] = filtros
            del options['filtros']

        for k in r_args:
            if k in ["valor", "agregacao", "ordenacao", "pivot", "calcs", "partition"]:
                options[k] = cls.extract_qry_param(r_args, k)
            elif k in ["as_image", "from_viewconf"]:
                val = False
                if r_args.get(k, False) == 'S':
                    val = True
                options[k] = val

        return options

    @staticmethod
    def extract_qry_param(params, param_name):
        ''' Extracts the given query param as an array of values '''
        if (param_name in params.keys() and
                params.get(param_name) is not None and
                params.get(param_name)):
            return params.get(param_name).split(',')
        return None

    @staticmethod
    def build_person_options(r_args, mod='empresa'):
        ''' Constrói as opções da pesquisa '''
        options = {}

        if 'dados' in r_args:
            options['column_family'] = r_args['dados']
        if 'competencia' in r_args:
            options['column'] = r_args['competencia']
        if 'id_pf' in r_args:
            options['id_pf'] = r_args['id_pf']
        if 'perspective' in r_args:
            options['perspective'] = r_args['perspective']
        if 'only_status' in r_args and r_args['only_status'] == 'S':
            options['only_status'] = True
        if 'reduzido' in r_args and r_args['reduzido'] == 'S':
            options['reduzido'] = True
        if 'pagina' in r_args:
            options['pagina'] = r_args['pagina']
        if 'por_pagina' in r_args:
            options['por_pagina'] = r_args['por_pagina']
        if 'pesquisa' in r_args:
            options['pesquisa'] = r_args['pesquisa']

        if mod == 'estabelecimento':
            options['cnpj_raiz'] = r_args['id_inv'][:-6]
            options['cnpj'] = r_args['id_inv']
        else:
            options['cnpj_raiz'] = r_args['id_inv']

        return options
