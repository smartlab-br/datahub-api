''' Repository para recuperar informações da CEE '''
from repository.base import ImpalaRepository

#pylint: disable=R0903
class ThematicRepository(ImpalaRepository):
    ''' Definição do repo '''
    TABLE_NAMES = {
        'MAIN': 'indicadores',
        'municipio': 'municipio',
        'sisben': 'sst_beneficio',
        'catweb': 'sst_cat',
        'incidenciaescravidao': 'incidencia_trabalho_escravo',
        'migracoesescravos': 'te_migracoes',
        'operacoesresgate': 'operacoes_trabalho_escravo'
    }
    JOIN_SUFFIXES = {
        'municipio': '_mun'
    }
    ON_JOIN = {
        'municipio': 'cd_mun_ibge = cd_municipio_ibge_dv'
    }
