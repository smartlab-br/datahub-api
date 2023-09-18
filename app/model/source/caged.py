''' Classes to create options dictionary for CAGED datasources '''
from model.source.base import BaseSource

class BaseCaged(BaseSource):
    ''' Base Option builder class for Caged datasources '''
    def get_options_rules_empresa(self, options, local_cols, df, persp):
        subset_rules = ["and", "eq-tipo_estab-1"]
        subset_rules.extend(
            self.get_context_options_empresa(options, local_cols, persp)
        )
        return subset_rules

class CagedSaldo(BaseCaged):
    ''' Option builder for Caged Saldo '''
    def get_options_empresa(self, options, local_cols, df, persp):
        ''' Create options according to tables and query conditions '''
        subset_rules = [
            f"eqlpint-{local_cols.get('cnpj')}-{options.get('cnpj_raiz')}-14-0-1-8"
        ]
        if options.get('column'):
            subset_rules.extend([
                "and", f"eq-{local_cols.get('compet')}-{options.get('column')}"
            ])
        subset_rules.extend(
            self.get_options_rules_empresa(options, local_cols, df, persp)
        )
        return {
            "categorias": ['\'1\'-pos'],
            "valor": ['qtd_admissoes', 'qtd_desligamentos', 'saldo_mov'],
            "agregacao": ['sum'],
            "where": subset_rules,
            "theme": df
        }        
