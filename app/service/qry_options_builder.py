''' Service para conversão de atributos de query para os objetos do fetch '''
class QueryOptionsBuilder():
    ''' Classe de serviço '''
    @classmethod
    def build_options(cls, r_args, rules = 'query'):
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

        if r_args.get('theme') is None and rules in ['query']:
            theme = 'MAIN'

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
