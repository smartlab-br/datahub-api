''' Stubs for model testing '''
import pandas as pd
from model.empresa.empresa import Empresa

class StubThematicModel():
    ''' Class to return a constant dataset when find_dataset is invoked '''
    def find_dataset(self, options):
        ''' Method to return a fixed collection '''
        return pd.DataFrame([
            {'cnpj': '12345678000101', 'compet': 2047, 'agr_count': 100},
            {'cnpj': '12345678000202', 'compet': 2099, 'agr_count': 200}
        ])
        
class StubEmpresa(Empresa):
    ''' Class to enable model testing without repository access '''    
    def get_thematic_handler(self):
        ''' Gets the stub thematic model instead of the real one '''
        return StubThematicModel()
