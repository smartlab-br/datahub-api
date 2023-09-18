'''Main tests in API'''
import unittest
from factory.source import SourceFactory
from model.source.base import BaseSource
from model.source.caged import CagedSaldo
# from model.source.caged import BaseCaged, CagedSaldo
# from model.source.aeronaves import Aeronaves
# from model.source.auto import Auto
# from model.source.catweb import Catweb
# from model.source.rais import Rais
# from model.source.renavam import Renavam
# from model.source.sisben import Sisben
# from model.source.rfb import BaseRfb, RfbSocios, RfbParticipacaoSocietaria
# from model.source.embarcacoes import Embarcacoes

class SourceModelCreateTest(unittest.TestCase):
    ''' Test behaviours linked to "empresa" dataset-specific model instantiation '''

    def test_instantiation_default_to_base_no_dataset(self):
        ''' Tests if create returns a base dataset model, when no dataset is sent '''
        chart = SourceFactory().create(None)
        self.assertTrue(isinstance(chart, BaseSource))

    def test_instantiation_default_to_base(self):
        ''' Tests if create returns a base dataset model, when a new dataset is sent '''
        chart = SourceFactory().create("non-specific")
        self.assertTrue(isinstance(chart, BaseSource))
        
    def test_instantiation_caged_saldo(self):
        ''' Tests if create returns a Caged Saldo dataset model '''
        chart = SourceFactory().create('cagedsaldo')
        self.assertTrue(isinstance(chart, CagedSaldo))
