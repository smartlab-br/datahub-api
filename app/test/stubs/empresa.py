''' Stubs for model testing '''
import pandas as pd
from datetime import datetime
from model.empresa.empresa import Empresa
from repository.empresa.pessoadatasets import PessoaDatasetsRepository
from repository.empresa.datasets import DatasetsRepository

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

class StubDatasetRepository(DatasetsRepository):
    ''' Class to unlock Empresa model testing that uses REDIS data '''
    DATASETS = {
        'skip': '2016',
        'test': '2017,2018',
        'failed_status': '2017,2099',
        'expired': '2017,2018',
        'another': '2019'
    }
    def load_and_prepare(self):
        ''' Avoids the application context '''

class StubPessoaDatasetRepository(PessoaDatasetsRepository):
    ''' Class to unlock Empresa model testing that uses REDIS data '''
    def load_and_prepare(self):
        ''' Avoids the application context '''

    def retrieve(self, _id_pfpj, dataframe, _pfpj='pj'):
        ''' Fakes a REDIS call and return static data '''
        str_now = datetime.strftime(datetime.now(), "%Y-%m-%d")
        if dataframe == 'unavailable':
            return {
                "2017": f"INGESTED|{str_now}",
                "2099": f"INGESTED|{str_now}",
                "when": f"{str_now}"
            }
        if dataframe == 'failed_status':
            return {
                "2017": f"FAILED|{str_now}",
                "2018": f"INGESTED|{str_now}",
                "when": f"{str_now}"
            }
        if dataframe == 'expired':
            return {
                "2017": "INGESTED|2000-01-01",
                "2018": "INGESTED|2000-01-01",
                "when": "2000-01-01"
            }
        return { # Valid
            "2017": f"INGESTED|{str_now}",
            "2018": f"INGESTED|{str_now}",
            "when": f"{str_now}"
        }

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

    def get_dataset_repo(self):
        ''' Gets the stub dataset repo instead of the real one '''
        return StubDatasetRepository()

    def get_pessoa_dataset_repo(self):
        ''' Gets the stub pessoa_dataset repo instead of the real one '''
        return StubPessoaDatasetRepository()
