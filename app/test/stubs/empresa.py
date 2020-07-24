''' Stubs for model testing '''
import pandas as pd
from model.empresa.empresa import Empresa

class StubThematicModel():
    ''' Class to return a constant dataset when find_dataset is invoked '''
    def find_dataset(self, options):
        ''' Method to return a fixed collection '''
        dataframe = [
            {'cnpj': '12345678000101', 'compet': 2047, 'agr_count': 100},
            {'cnpj': '12345678000202', 'compet': 2099, 'agr_count': 200}
        ]
        if not options.get('as_pandas', True) and not options.get('no_wrap', True):
            return {
                "metadata": {"fonte": "Fonte"},
                "dataset": dataframe
            }
        return pd.DataFrame(dataframe)

    def get_persp_columns(self, dataframe):
        ''' Returns a fixed perspective column for testing '''
        return 'persp_column'
        
class StubEmpresa(Empresa):
    ''' Class to enable model testing without repository access '''
    EXPECTED_GROUPED_STATS = {
        'stats_estab': {
            '12345678000101': {'agr_count': 100, 'compet': 2047},
            '12345678000202': {'agr_count': 200, 'compet': 2099}
        },
        'stats_compet': {
            '2047': {'agr_count': 100, 'cnpj': '12345678000101'},
            '2099': {'agr_count': 200, 'cnpj': '12345678000202'}
        },
        'stats_estab_compet': {
            '2047_12345678000101': {
                'agr_count': 100, 'cnpj': '12345678000101', 'compet': 2047
            },
            '2099_12345678000202': {
                'agr_count': 200, 'cnpj': '12345678000202', 'compet': 2099
            }
        }
    }
    def get_thematic_handler(self):
        ''' Gets the stub thematic model instead of the real one '''
        return StubThematicModel()
