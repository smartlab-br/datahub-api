''' Classes to create options dictionary for Autos de Infração datasources '''
from model.source.base import BaseSource

class Auto(BaseSource):
    ''' Base Option builder class for Autos de Infração datasources '''
    def get_options_rules_empresa(self, options, local_cols, df, persp):
        subset_rules = [
            "and", f"eq-tpinscricao-'1'",
            "and", f"nl-dtcancelamento"
        ]
        subset_rules.extend(
            self.get_context_options_empresa(options, local_cols, persp)
        )
        return subset_rules