''' Classes to create options dictionary for RFB datasources '''
from model.source.base import BaseSource

class BaseRfb(BaseSource):
    ''' Base Option builder class for Caged datasources '''
    def get_options_empresa(self, options, local_cols, df, persp):
        ''' Create options according to tables and query conditions '''
        subset_rules = [f"eq-{local_cols.get('cnpj_raiz')}-{options.get('cnpj_raiz')}"]
        subset_rules.extend(self.get_options_rules_empresa(options, local_cols, df, persp))
        return {
            "categorias": ['\'1\'-pos'],
            "agregacao": ['count'],
            "where": subset_rules,
            "theme": df
        }

class RfbSocios(BaseRfb):
    ''' Option builder for Caged Saldo '''
    def get_options_empresa(self, options, local_cols, df, persp):
        ''' Create options according to tables and query conditions '''
        subset_rules = [
            f"eqlponstr-{local_cols.get('cnpj_raiz')}-{options.get('cnpj_raiz')}-8-0-1-8"
        ]
        subset_rules.extend(self.get_options_rules_empresa(options, local_cols, df, persp))
        return {
            "categorias": ['\'1\'-pos'],
            "agregacao": ['count'],
            "where": subset_rules,
            "theme": df
        }

class RfbParticipacaoSocietaria(BaseRfb):
    ''' Option builder for Caged Saldo '''
    def get_options_empresa(self, options, local_cols, df, persp):
        ''' Create options according to tables and query conditions '''
        subset_rules = [
            f"eqlponstr-{local_cols.get('cnpj_raiz')}-{options.get('cnpj_raiz')}-14-0-1-8"
        ]
        subset_rules.extend(self.get_options_rules_empresa(options, local_cols, df, persp))
        return {
            "categorias": ['\'1\'-pos'],
            "agregacao": ['count'],
            "where": subset_rules,
            "theme": df
        }
