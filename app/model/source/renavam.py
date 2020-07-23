''' Classes to create options dictionary for Renavam datasources '''
from model.source.base import BaseSource

class Renavam(BaseSource):
    ''' Base Option builder class for Renavam datasources '''
    def get_options_empresa(self, options, local_cols, df, persp):
        ''' Create options according to tables and query conditions '''
        subset_rules = [
            f"eq-{local_cols.get('cnpj_raiz')}-'{options.get('cnpj_raiz')}'-1-8",
            "and",
            f"eqsz-{local_cols.get('cnpj_raiz')}-14"
        ]
        subset_rules.extend(self.get_options_rules_empresa(options, local_cols, df, persp))
        return {
            "categorias": [local_cols.get('cnpj_raiz')],
            "agregacao": ['count'],
            "where": subset_rules,
            "theme": df
        }
