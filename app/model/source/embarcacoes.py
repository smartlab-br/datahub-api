''' Classes to create options dictionary for Embarcacoes datasources '''
from model.source.base import BaseSource

class Embarcacoes(BaseSource):
    ''' Base Option builder class for Embarcacoes datasources '''
    def get_options_rules_empresa(self, options, local_cols, df, persp):
        subset_rules = [
            "and", f"ne-{local_cols.get('cnpj')}-'00000000000000'"
        ]
        subset_rules.extend(
            self.get_context_options_empresa(options, local_cols, persp)
        )
        return subset_rules