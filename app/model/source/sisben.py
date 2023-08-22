''' Classes to create options dictionary for Sisben datasources '''
from model.source.base import BaseSource

class Sisben(BaseSource):
    ''' Base Option builder class for Sisben datasources '''
    def get_options_rules_empresa(self, options, local_cols, df, persp):
        subset_rules = [
            "and", f"ne-cast({local_cols.get('cnpj')} as INT)-0",
            "and", "eq-tp_empregador-1"
        ]
        subset_rules.extend(
            self.get_context_options_empresa(options, local_cols, persp)
        )
        return subset_rules
    
    def get_options_empresa(self, options, local_cols, df, persp):
        ''' Create options according to tables and query conditions '''
        subset_rules = [
            f"eq-{local_cols.get('cnpj_raiz')}-'{options.get('cnpj_raiz')}'"
        ]
        if options.get('column'):
            subset_rules.extend([
                "and", f"eq-cast({local_cols.get('compet')} as INT)-{options.get('column')}"
            ])
        subset_rules.extend(self.get_options_rules_empresa(options, local_cols, df, persp))
        return {
            "categorias": [local_cols.get('cnpj_raiz')],
            "agregacao": ['count'],
            "where": subset_rules,
            "theme": f'{df}_c' # Disambiguation
        }
