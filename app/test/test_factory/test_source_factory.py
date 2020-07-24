'''Main tests in API'''
import unittest
from factory.source import SourceFactory
from model.source.base import BaseSource
from model.source.caged import BaseCaged, CagedSaldo
from model.source.aeronaves import Aeronaves
from model.source.auto import Auto
from model.source.catweb import Catweb
from model.source.rais import Rais
from model.source.renavam import Renavam
from model.source.sisben import Sisben
from model.source.rfb import BaseRfb, RfbSocios, RfbParticipacaoSocietaria

class SourceModelCreateTest(unittest.TestCase):
    ''' Test behaviours linked to "empresa" dataset-specific model instantiation '''
    def test_instantiation_caged_saldo(self):
        ''' Tests if create returns a Caged Saldo dataset model '''
        chart = SourceFactory().create('cagedsaldo')
        self.assertTrue(isinstance(chart, CagedSaldo))

    def test_instantiation_caged_trabalhador(self):
        ''' Tests if create returns a Base Caged dataset model for cagedtrabalhador '''
        chart = SourceFactory().create('cagedtrabalhador')
        self.assertTrue(isinstance(chart, BaseCaged))

    def test_instantiation_caged_trabalhador_ano(self):
        ''' Tests if create returns a Base Caged dataset model for cagedtrabalhadorano '''
        chart = SourceFactory().create('cagedtrabalhadorano')
        self.assertTrue(isinstance(chart, BaseCaged))

    def test_instantiation_aeronaves(self):
        ''' Tests if create returns a Aeronaves dataset model '''
        chart = SourceFactory().create('aeronaves')
        self.assertTrue(isinstance(chart, Aeronaves))

    def test_instantiation_auto(self):
        ''' Tests if create returns a Auto dataset model '''
        chart = SourceFactory().create('auto')
        self.assertTrue(isinstance(chart, Auto))

    def test_instantiation_catweb(self):
        ''' Tests if create returns a CATWEB dataset model '''
        chart = SourceFactory().create('catweb')
        self.assertTrue(isinstance(chart, Catweb))

    def test_instantiation_rais(self):
        ''' Tests if create returns a RAIS dataset model '''
        chart = SourceFactory().create('rais')
        self.assertTrue(isinstance(chart, Rais))

    def test_instantiation_renavam(self):
        ''' Tests if create returns a Renavam dataset model '''
        chart = SourceFactory().create('renavam')
        self.assertTrue(isinstance(chart, Renavam))

    def test_instantiation_sisben(self):
        ''' Tests if create returns a SISBEN dataset model '''
        chart = SourceFactory().create('sisben')
        self.assertTrue(isinstance(chart, Sisben))

    def test_instantiation_rfb_socios(self):
        ''' Tests if create returns a RFB-Socios dataset model '''
        chart = SourceFactory().create('rfbsocios')
        self.assertTrue(isinstance(chart, RfbSocios))

    def test_instantiation_rfb_participacao_societaria(self):
        ''' Tests if create returns a RFB-Participacao-Societaria dataset model '''
        chart = SourceFactory().create('rfbparticipacaosocietaria')
        self.assertTrue(isinstance(chart, RfbParticipacaoSocietaria))

    def test_instantiation_rfb(self):
        ''' Tests if create returns a base RFB dataset model '''
        chart = SourceFactory().create('rfb')
        self.assertTrue(isinstance(chart, BaseRfb))

    def test_instantiation_default_to_base_no_dataset(self):
        ''' Tests if create returns a base dataset model, when no dataset is sent '''
        chart = SourceFactory().create(None)
        self.assertTrue(isinstance(chart, BaseSource))

    def test_instantiation_default_to_base(self):
        ''' Tests if create returns a base dataset model, when a new dataset is sent '''
        chart = SourceFactory().create("non-specific")
        self.assertTrue(isinstance(chart, BaseSource))
