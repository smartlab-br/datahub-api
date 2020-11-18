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
        'sstcats': 'sst_cat',
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

        'rais': 'compliance.tb_rais',
        'rfb': "compliance.rfb_dados_cadastrais_2018",
        'sisben_c': "compliance.concessao_2018",
        'catweb_c': "compliance.catweb",
        'auto': "compliance.tb_auto",
        'auto_trabalhadores': "compliance.tb_auto_trabalhador",
        'caged': "compliance.tb_caged_estab",
        'rfbsocios': "compliance.rfb_dados_socios_tratado",
        'rfbparticipacaosocietaria': "compliance.rfb_dados_socios_tratado",
        'aeronaves': "compliance.tb_aeronaves",
        'renavam': "compliance.tb_renavam_2018",
        'cagedsaldo': "compliance.tb_caged_saldos",
        'cagedtrabalhador': "compliance.tb_caged_trabalhador",
        'cagedtrabalhadorano': "compliance.tb_caged_trabalhador",

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

        'estabelecimentocnes': 'estabelecimento_cnes',
        'srag': 'srag',
        'covidcasos': 'covid_casos',
        'covidarranjoregic': 'covid_arranjo_regic',
        'covidclassempt': 'covid_classe_mpt',
        'coviddenunciampt': 'covid_denuncia_mpt',
        'coviddenunciacnpjmpt': 'covid_denuncia_cnpj_mpt',
        'coviddocumentompt': 'covid_documento_mpt',
        'covidtemampt': 'covid_tema_mpt',
        'coviddestinacaompt': 'covid_destinacao_mpt',

        'cagedtermometro': 'caged_termometro'
    }
    DEFAULT_PARTITIONING = {
        'MAIN': 'cd_indicador',
        'NONE': [
            'municipio', 'assistenciasocial', 'sisben', 'catweb',
            'censoagronacional', 'censoagroestadual', 'censoagromunicipal',
            'coviddenunciampt', 'coviddocumentompt', 'coviddestinacaompt'
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
        if options is None:
            return self.DEFAULT_PARTITIONING['MAIN']
        if 'theme' not in options:
            return self.DEFAULT_PARTITIONING.get('MAIN')
        if options.get('theme') in self.DEFAULT_PARTITIONING:
            return self.DEFAULT_PARTITIONING.get(options.get('theme'))
        if options.get('theme') in self.DEFAULT_PARTITIONING.get('NONE'):
            return ''
        return self.DEFAULT_PARTITIONING.get('MAIN')
