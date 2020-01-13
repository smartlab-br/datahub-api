''' Repository para recuperar informações da CEE '''
from repository.base import ImpalaRepository

#pylint: disable=R0903
class ThematicRepository(ImpalaRepository):
    ''' Definição do repo '''
    TABLE_NAMES = {
        'MAIN': 'indicadores',
        'municipio': 'municipio',

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
        
        'estadicmunic': 'estadic_munic',
        'estadicuf': 'estadic_munic_uf',
        'estadicunidadempt': 'estadic_munic_mpt_unidade',

        'mapear': 'mapear',
        'provabrasil': 'ti_prova_brasil',
        'tiindicadoresnacionais': 'ti_indicadores_br',
        'tiindicadoresmunicipais': 'ti_indicadores_mun',
        'tiindicadoresestaduais': 'ti_indicadores_uf',
        'tiindicadoresunidadempt': 'ti_indicadores_mpt_unidade',
        'censoagromunicipal': 'censo_agro',
        'censoagroestadual': 'censo_agro_uf',
        'censoagronacional': 'censo_agro_br',

        'incidenciaescravidao': 'incidencia_trabalho_escravo',
        'migracoesescravos': 'te_migracoes',
        'operacoesresgate': 'operacoes_trabalho_escravo'
    }
    DEFAULT_PARTITIONING = {
        'MAIN': 'cd_indicador',
        'NONE': [
            'municipio', 'assistenciasocial', 'sisben', 'catweb',
            'censoagronacional', 'censoagroestadual', 'censoagromunicipal'
        ]
    }
    JOIN_SUFFIXES = {
        'municipio': '_mun'
    }
    ON_JOIN = {
        'municipio': 'cd_mun_ibge = cd_municipio_ibge_dv'
    }

    def get_default_partitioning(self, options):
        if 'theme' not in options:
            return self.DEFAULT_PARTITIONING['MAIN']
        elif options['theme'] self.DEFAULT_PARTITIONING:
            return self.DEFAULT_PARTITIONING[options['theme']]
        elif options['theme'] self.DEFAULT_PARTITIONING['NONE']
            return ''
        return self.DEFAULT_PARTITIONING['MAIN']
