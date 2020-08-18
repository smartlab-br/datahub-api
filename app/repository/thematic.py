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
        'ticensoagromunicipal': 'censo_agro',
        'ticensoagroestadual': 'censo_agro_uf',
        'ticensoagronacional': 'censo_agro_br',

        'incidenciaescravidao': 'incidencia_trabalho_escravo',
        'migracoesescravos': 'te_migracoes',
        'operacoesresgate': 'operacoes_trabalho_escravo',
        'teindicadoresnacionais': 'te_indicadores_br',
        'teindicadoresmunicipais': 'te_indicadores_mun',
        'teindicadoresestaduais': 'te_indicadores_uf',
        'teindicadoresunidadempt': 'te_indicadores_mpt_unidade',
        'temlexposicaoresgate': 'te_exposicao_rgt_mun',
        'temlexposicaoresgatefeatures': 'te_exposicao_rgt_feat_importance_mun',
        'temlexposicaonaturais': 'te_exposicao_nat_mun',
        'temlexposicaonaturaisfeatures': 'te_exposicao_nat_feat_importance_mun',

        'casoscovid19': 'casos_covid_19',
        'estabelecimentocnes': 'estabelecimento_cnes',
        'arranjoregic': 'arranjo_regic',
        'srag': 'srag',
        'classemptcovid19': 'classe_mpt_covid_19',
        'denunciamptcovid19': 'denuncia_mpt_covid_19',
        'documentomptcovid19': 'documento_mpt_covid_19',
        'temamptcovid19': 'tema_mpt_covid_19'
    }
    DEFAULT_PARTITIONING = {
        'MAIN': 'cd_indicador',
        'NONE': [
            'municipio', 'assistenciasocial', 'sisben', 'catweb',
            'censoagronacional', 'censoagroestadual', 'censoagromunicipal'
        ],
        'provabrasil': 'cd_tr_fora'
    }
    JOIN_SUFFIXES = {
        'municipio': '_mun'
    }
    ON_JOIN = {
        'municipio': 'cd_mun_ibge = cd_municipio_ibge_dv'
    }

    def get_default_partitioning(self, options):
        ''' Gets default partitioning from thematic datasets' definition '''
        if 'theme' not in options:
            return self.DEFAULT_PARTITIONING['MAIN']
        if options['theme'] in self.DEFAULT_PARTITIONING:
            return self.DEFAULT_PARTITIONING[options['theme']]
        if options['theme'] in self.DEFAULT_PARTITIONING['NONE']:
            return ''
        return self.DEFAULT_PARTITIONING['MAIN']
