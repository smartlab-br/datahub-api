''' Classes to create options dictionary for RAIS datasources '''
from model.source.base import BaseSource

class Rais(BaseSource):
    ''' Base Option builder class for RAIS datasources '''
    def get_options_rules_empresa(self, options, local_cols, df, persp):
        subset_rules = [
            "and", f"eq-tp_estab-1"
        ]
        subset_rules.extend(
            self.get_context_options_empresa(options, local_cols, persp)
        )
        return subset_rules
