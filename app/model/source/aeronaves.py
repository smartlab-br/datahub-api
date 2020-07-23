''' Classes to create options dictionary for Aeronaves datasources '''
from model.source.base import BaseSource

class Aeronaves(BaseSource):
    ''' Base Option builder class for Aeronaves datasources '''
    def get_options_empresa(self, options, local_cols, df, persp):
        ''' Create options according to tables and query conditions '''
        subset_rules = [
            f"eqon-{local_cols.get('cnpj_raiz')}-{options.get('cnpj_raiz')}-1-8",
            "and",
            f"neon-{local_cols.get('cnpj_raiz')}-00000000000000"
        ]
        subset_rules.extend(self.get_options_rules_empresa(options, local_cols, df, persp))
        return {
            "categorias": [local_cols.get('cnpj_raiz')],
            "agregacao": ['count'],
            "where": subset_rules,
            "theme": df
        }
