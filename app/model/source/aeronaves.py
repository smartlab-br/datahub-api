''' Classes to create options dictionary for Aeronaves datasources '''
from model.source.base import BaseSource

class Aeronaves(BaseSource):
    ''' Base Option builder class for Aeronaves datasources '''
    def get_options_rules_empresa(self, options, local_cols, df, persp):
        subset_rules = [
            "and", f"ne-cast({local_cols.get('cnpj')} as INT)-0"
        ]
        subset_rules.extend(
            self.get_context_options_empresa(options, local_cols, persp)
        )
        return subset_rules