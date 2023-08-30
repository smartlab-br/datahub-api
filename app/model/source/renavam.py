''' Classes to create options dictionary for Renavam datasources '''
from model.source.base import BaseSource

class Renavam(BaseSource):
    ''' Base Option builder class for Renavam datasources '''
    def get_options_rules_empresa(self, options, local_cols, df, persp):
        subset_rules = [
            "and", f"ne-cast({local_cols.get('cnpj')} as BIGINT)-0"
        ]
        subset_rules.extend(
            self.get_context_options_empresa(options, local_cols, persp)
        )
        return subset_rules