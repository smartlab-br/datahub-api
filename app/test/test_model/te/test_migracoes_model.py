'''Main tests in API'''
import unittest
import pandas as pd
from model.te.migracoes import MigracoesEscravo


class StubMigracoesModel(MigracoesEscravo):
    ''' Classe de STUB da abstração de models '''
    METADATA = {
        "fonte": 'Instituto STUB'
    }

    DATASET = [{'source': 'Porto Velho/RO', 'target': 'Rio Branco/AC', 'agr_count': 2}]

    def __init__(self):
        ''' Construtor '''
        self.sankey_ds = None

    def get_repo(self):
        ''' Método abstrato para carregamento do repositório '''
        return 'My repo'

    def fetch_metadata(self, options=None):
        return self.METADATA

    def find_dataset(self, options):
        return pd.DataFrame(self.DATASET)

class MigracoesEscravoModelFindDatasetSankeyTest(unittest.TestCase):
    ''' Classe que testa a obtenção dos dados passados para o gráfico sankey. '''
    def test_find_dataset_sankey(self):
        ''' Verifica se retorna exatamente o atributo definido no model '''
        model = StubMigracoesModel()
        expected = {
            "metadata": StubMigracoesModel.METADATA,
            "dataset": StubMigracoesModel.DATASET
        }
        self.assertEqual(model.find_dataset_sankey({}), expected)