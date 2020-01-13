''' Repository para recuperar informações da CEE '''
from repository.base import ImpalaRepository

#pylint: disable=R0903
class ThematicRepository(ImpalaRepository):
    ''' Definição do repo '''
    TABLE_NAMES = {
        'MAIN': 'indicadores',
        'municipio': 'municipio',
        'incidenciaescravidao': 'incidencia_trabalho_escravo',
        'migracoesescravos': 'te_migracoes',
        'operacoesresgate': 'operacoes_trabalho_escravo'
        'indicadoresestaduais': 'indicadores_uf',
        'indicadoresmesorregionais': 'indicadores_mesorregiao',
        'indicadoresmicrorregionais': 'indicadores_microrregiao',
        'indicadoresmptunidades': 'indicadores_mpt_unidades',
        'indicadoresmunicipais': 'indicadores',
        'indicadoresnacionais': 'indicadores_br',
        'indicadoresregionais': 'indicadores_regiao',
        'assistenciasocial': 'orgs_assistencia_social',
        'sisben': 'sst_beneficio',
        'catweb': 'sst_cat',
        'sstindicadoresnacionais': 'sst_indicadores_br', 
        'sstindicadoresmunicipais': 'sst_indicadores_mun', 
        'sstindicadoresestaduais': 'sst_indicadores_mun', 
        'sstindicadoresunidadempt': 'sst_indicadores_mpt_unidade',

    }
    DEFAULT_PARTITIONING = {
        'MAIN': 'cd_indicador',
        'municipio': '',
        'assistenciasocial': '',
        'incidenciaescravidao': 'incidencia_trabalho_escravo',
        'migracoesescravos': 'te_migracoes',
        'operacoesresgate': 'operacoes_trabalho_escravo'
        'sisben': '',
        'catweb': '',
    }
    JOIN_SUFFIXES = {
        'municipio': '_mun'
    }
    ON_JOIN = {
        'municipio': 'cd_mun_ibge = cd_municipio_ibge_dv'
    }

    def get_default_partitioning(self, options):
        if 'theme' not in options or options['theme'] not in self.DEFAULT_PARTITIONING:
            return self.DEFAULT_PARTITIONING['MAIN']
        return self.DEFAULT_PARTITIONING[options['theme']]